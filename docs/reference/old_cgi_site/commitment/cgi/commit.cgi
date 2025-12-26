#!/usr/bin/perl
#
# Person database maintenance.
#
# Author: Kayvan Sylvan
#
use lib "/home/kayvan/perl5/lib/perl5";
use lib "/home/kayvan/public_html/afg/commitment/modules";
use lib "/home/kayvan/perl/local/lib/perl5/site_perl/5.10.0";
use Person;
use Event;
use CGI qw(-debug -no_xhtml); # Perl CGI scripting.
use CGI::Carp 'fatalsToBrowser'; # Report errors to browser, not just server log
use strict;

my $q = new CGI; # The query object
my $person = new Person("/home/kayvan/public_html/afg/commitment/save/persons.db", "|");
my $event = new Event("/home/kayvan/public_html/afg/commitment/save/events.db", "|");
my $mode = defined($q->param('mode')) ? $q->param('mode') : "login";
my %cookie_values = ( session_id => 0, user => undef );
my $has_cookie = 0;
my $login_is_good = 0;
use utils; # generic utilities module
use MyConfig;
#
# These constants are used in the commitment table.
#
my $background_color = '#FFFFFF'; # For non-selected events (white)
my $selected_color = '#FFFF66'; # For selected events (yellow).
my $unselected_color = '#FFB6C1'; # For definite NO (pink).
if (!defined($q->param('ignore_cookie'))) {
    my %tmp_values = $q->cookie('commitme');
    if (defined($q->cookie('commitme')) {
        %cookie_values = %tmp_values;
        $has_cookie = 1;
    }
}
# Change initial mode
$mode = 'begin' if (($mode eq 'login') && ($cookie_values{session_id}));
if ($mode eq "login") {
    %cookie_values = ( session_id => 0 );
    my $cookie = $q->cookie(-name => 'commitme',
        -value=>\%cookie_values, -expires=>'+21d');
    print $q->header(-cookie=>$cookie),
        $q->start_html(-title=>'CommitMe', -bgcolor=>'#FFFFFF'),
        $q->center($q->h1('CommitMe!')), $q->hr();
    $q->param('mode', 'begin');
    print $q->start_form(), $q->start_center(),
        "Login: ", $q->textfield(-name=>'login', -size=>20, -maxlength=>20), $q->p(),
        "Password: ", $q->password_field(-name=>'password', -size=>20, -maxlength=>20);
    print $q->p(), $q->submit(-name=>'Submit', -value=>"Login Now!"),
        $q->end_center(), $q->hidden(-name=>'mode', -default=>'begin'),
        $q->end_form();
} else {
    if ($cookie_values{session_id}) {
        if ($person->restore($cookie_values{user})) {
            $login_is_good = 1;
        } else {
            $cookie_values{session_id} = 0;
        }
    }
    if (!$cookie_values{session_id}) {
        if ($person->restore($q->param('login'))) { # User found
            $login_is_good = $person->check_passwd($q->param('password'));
        } else {
            $login_is_good = 0;
        }
    }
    if ($login_is_good && $person->admin_level() && $q->param('other_login')) {
        $login_is_good = $person->restore($q->param('other_login'));
    }
    if ($login_is_good) {
        $cookie_values{user} = $person->login()
          if (!defined($cookie_values{user}));
        $cookie_values{session_id} = $$;
        my $cookie = $q->cookie(-name => 'commitme',
            -value=>\%cookie_values, -expires=>'+21d');
        print $q->header(-cookie=>$cookie),
            $q->start_html(-title=>'CommitMe', -bgcolor=>'#FFFFFF'),
            $q->center($q->h1('CommitMe!')), $q->hr();
        my %all_params = $q->Vars();
        my @_ev_list = grep(/^_ev_/, keys %all_params);
        my $temp_changed = 0;
        foreach my $varname (@_ev_list) {
            my $temp_id = substr($varname, 4);
            next if (!$event->restore($temp_id)); # Can only happen rarely!
            if ($q->param($varname) eq "Yes") {
                if ($person->is_committed($event) != 1) {
                    $person->commit($event); $temp_changed = 1;
                }
            } elsif ($q->param($varname) eq "No") {
                if ($person->is_committed($event) != -1) {
                    $person->commit($event, -1); $temp_changed = 1;
                }
            } else {
                if ($person->is_committed($event)) { # decided
                    $person->uncommit($event); $temp_changed = 1;
                }
            }
        }
        $person->save() if $temp_changed; # Only save the Person object if changed
        if ($mode ne 'admin_begin') {
            my $fix_name = $person->full_name();
            $fix_name =~ s/(.*), (.*)/$2 $1/;
            print $q->h1("Welcome, ".$fix_name."!");
            if (($mode ne 'prefs') && ($mode ne 'set_prefs')) {
                if ($person->inactive()) {
                    my $extra_url = $has_cookie ? "" :
                        "login=".$q->param('login').";"."password=".$q->param('password');
                    my $tmp_link = $q->url(-relative=>1)."?mode=prefs;".$extra_url;
                    print $q->h2($q->i("You are marked as inactive! Click ".
                        $q->a({-href=>$tmp_link}, $q->b("here")). " to change that."));
                }
            }
        } else {
            my $orig_person = new Person("/home/kayvan/public_html/afg/commitment/save/persons.db", "|");
            if (!$orig_person->restore($q->param('login'))) {
                if ($has_cookie) {
                    $orig_person->restore($cookie_values{user});
                }
            }
            my $fix_name = $orig_person->full_name();
            $fix_name =~ s/(.*), (.*)/$2 $1/;
            print $q->h1("Welcome back, ".$fix_name.".");
            $fix_name = $person->full_name();
            $fix_name =~ s/(.*), (.*)/$2 $1/;
            print $q->h1("You are editing commitments for ".$fix_name.".");
        }
        if ($mode eq 'begin') { 
            print $q->p(), $q->p();
            my $extra_url = $has_cookie ? "" :
                "login=".$q->param('login').";"."password=".$q->param('password');
            my $home = $q->url(-relative=>1)."?mode=begin;".$extra_url;
            my $login_screen = $q->url(-relative=>1)."?mode=login;ignore_cookie=1";
            my $prefs = $q->url(-relative=>1)."?mode=prefs;".$extra_url;
            print $q->p(), $q->start_center(), $q->start_table({-border=>1}); 
            print $q->Tr($q->td([
                $q->a({-href=>"$prefs"}, "Login Preferences"),
                "&nbsp;" x 20,
                $q->a({-href=>"$home"}, "Personal Summary"),
                "&nbsp;" x 20,
                $q->a({-href=>"$login_screen"}, "Login Again")
            ])), $q->end_table(), $q->end_center();
            print $q->p();
            my $config = new MyConfig("/home/kayvan/public_html/afg/commitment/save/config.db", "|");
            print $q->p(), $q->start_center(), $q->start_table({-border=>1});
            my @navbar_links = ();
            my @tmp;
            $config->restore_where('key =~ /^navbar_url/', 'key ASC');
            while ($config->restore_next()) {
                @tmp = split('\*', $config->val()); # Description*URL
                if ($#tmp == 1) {
                    push(@navbar_links, $q->a({-href=>$tmp[1]}, $tmp[0]));
                } else {
                    push(@navbar_links, "BAD LINK: ", $config->val());
                }
            }
            print $q->Tr($q->td([@navbar_links]));
            print $q->end_table(), $q->end_center();
            print $q->h3("Instructions: Enter your changes to all events.
                When finished, click on the ENTER COMMITMENTS button  to save
                your changes."), $q->p(), "\n";
            print $q->h2("Your Personal Commitments are:"), $q->start_form();
            print $q->p(),
                $q->center($q->submit(-name=>"Submit", -value=>"ENTER COMMITMENTS")), "<p>\n";
            my $now_date_time = new Persistent::DataType::DateTime('now');
            my $now_time = $now_date_time->value(); # Get the string
            my @current_events = ();
            $event->restore_all('event_time ASC'); # Sort the events by date!
            while ($event->restore_next()) {
                if ($now_time le $event->event_time()) {
                    push @current_events, $event->id();
                }
            }
            my $number_of_events = $#current_events + 1;
            if ($number_of_events) {
                print $q->start_center(), $q->start_table({-border=>undef}),
                    $q->caption($number_of_events . " events in database.");
                print $q->Tr({-align=>"CENTER"},
                    $q->th(["Description", "Date and Time", "Arrive By", "Committed"]));
                foreach my $event_id (@current_events) {
                    next if (!$event->restore($event_id)); # Only can happen if id was deleted!
                    my $show_event_url = $q->url(-relative=>1)."?mode=show_event;event_id=".$event_id;
                    my $desc = $event->description();
                    if ($event->location()) { $desc .= " (At ".$event->location.")"; }
                    my $row_color = ($person->is_committed($event) == 1) ? $selected_color : 
                                     $background_color;
                    $row_color = ($person->is_committed($event) == -1) ? $unselected_color : $row_color;
                    $show_event_url .= ";login=".$q->param('login').";password=".$q->param('password');
                    my $a_tag = $q->a({-href=>$show_event_url},$desc);
                    print $q->Tr({-align=>"CENTER"},
                        $q->td({-bgcolor=>$row_color},
                            [$a_tag, time_display($event->event_time()),
                            time_display($event->arrive_by(), 2), $q->popup_menu(-name=>"_ev_".$event->id(),
                                                                      -values=>["Yes", "No", "Undecided"],
                                                                      -default=>(($person->is_committed($event) == 1) ? "Yes" : 
                                                                                 (($person->is_committed($event) == -1) ? "No" : "Undecided")))]));
                }
                print $q->end_table(), $q->end_center();
            } else {
                print $q->p(), $q->p(), "There are no upcoming events, sorry!";
            };
            print $q->p(),
                $q->center($q->submit(-name=>"Submit", -value=>"ENTER COMMITMENTS")),
                $q->hidden(-name=>'mode', -default=>'begin'),
                $q->hidden(-name=>'login', -default=>$q->param('login')),
                $q->hidden(-name=>'password', -default=>$q->param('password')),
                $q->end_form();
            my $extra_url = $has_cookie ? "" :
                "login=".$q->param('login').";"."password=".$q->param('password');
            my $home = $q->url(-relative=>1)."?mode=begin;".$extra_url;
            my $login_screen = $q->url(-relative=>1)."?mode=login;ignore_cookie=1";
            my $prefs = $q->url(-relative=>1)."?mode=prefs;".$extra_url;
            print $q->p(), $q->start_center(), $q->start_table({-border=>1}); 
            print $q->Tr($q->td([
                $q->a({-href=>"$prefs"}, "Login Preferences"),
                "&nbsp;" x 20,
                $q->a({-href=>"$home"}, "Personal Summary"),
                "&nbsp;" x 20,
                $q->a({-href=>"$login_screen"}, "Login Again")
            ])), $q->end_table(), $q->end_center();
            print $q->p();
            my $config = new MyConfig("/home/kayvan/public_html/afg/commitment/save/config.db", "|");
            print $q->p(), $q->start_center(), $q->start_table({-border=>1});
            my @navbar_links = ();
            my @tmp;
            $config->restore_where('key =~ /^navbar_url/', 'key ASC');
            while ($config->restore_next()) {
                @tmp = split('\*', $config->val()); # Description*URL
                if ($#tmp == 1) {
                    push(@navbar_links, $q->a({-href=>$tmp[1]}, $tmp[0]));
                } else {
                    push(@navbar_links, "BAD LINK: ", $config->val());
                }
            }
            print $q->Tr($q->td([@navbar_links]));
            print $q->end_table(), $q->end_center();
            if ($person->admin_level()) {
                $q->param('mode', 'admin_begin');
                print $q->p(), $q->hr(), $q->start_form(), "Other login: ",
                    $q->textfield(-name=>'other_login', -size=>20, -maxlength=>20),
                    $q->i("&nbsp(Enter another login name here to edit their commitments)"),
                    $q->submit(-name=>"Edit", -value=>"Edit"),
                    $q->hidden(-name=>'login', -default=>$q->param('login')),
                    $q->hidden(-name=>'password', -default=>$q->param('password')),
                    $q->hidden(-name=>'mode', -default=>'admin_begin'),
                    $q->end_form();
            }
        }
        if ($mode eq 'admin_begin') { 
            print $q->p(), $q->p();
            print $q->h2("The Commitments for ".$person->full_name()." are:");
            print $q->start_form();
            my $now_date_time = new Persistent::DataType::DateTime('now');
            my $now_time = $now_date_time->value(); # Get the string
            my @current_events = ();
            $event->restore_all('event_time ASC'); # Sort the events by date!
            while ($event->restore_next()) {
                if ($now_time le $event->event_time()) {
                    push @current_events, $event->id();
                }
            }
            my $number_of_events = $#current_events + 1;
            if ($number_of_events) {
                print $q->start_center(), $q->start_table({-border=>undef}),
                    $q->caption($number_of_events . " events in database.");
                print $q->Tr({-align=>"CENTER"},
                    $q->th(["Description", "Date and Time", "Arrive By", "Committed"]));
                foreach my $event_id (@current_events) {
                    next if (!$event->restore($event_id)); # Only can happen if id was deleted!
                    my $show_event_url = $q->url(-relative=>1)."?mode=show_event;event_id=".$event_id;
                    my $desc = $event->description();
                    if ($event->location()) { $desc .= " (At ".$event->location.")"; }
                    my $row_color = ($person->is_committed($event) == 1) ? $selected_color : 
                                     $background_color;
                    $row_color = ($person->is_committed($event) == -1) ? $unselected_color : $row_color;
                    $show_event_url .= ";login=".$q->param('login').";password=".$q->param('password');
                    my $a_tag = $q->a({-href=>$show_event_url},$desc);
                    print $q->Tr({-align=>"CENTER"},
                        $q->td({-bgcolor=>$row_color},
                            [$a_tag, time_display($event->event_time()),
                            time_display($event->arrive_by(), 2), $q->popup_menu(-name=>"_ev_".$event->id(),
                                                                      -values=>["Yes", "No", "Undecided"],
                                                                      -default=>(($person->is_committed($event) == 1) ? "Yes" : 
                                                                                 (($person->is_committed($event) == -1) ? "No" : "Undecided")))]));
                }
                print $q->end_table(), $q->end_center();
            } else {
                print $q->p(), $q->p(), "There are no upcoming events, sorry!";
            };
            print $q->p(),
                $q->center($q->submit(-name=>"Submit", -value=>"Enter Commitments")),
                $q->hidden(-name=>'mode', -default=>'admin_begin'),
                $q->hidden(-name=>'login', -default=>$q->param('login')),
                $q->hidden(-name=>'password', -default=>$q->param('password')),
                $q->hidden(-name=>'other_login', -default=>$q->param('other_login')),
                $q->end_form();
        }
        if ($mode eq 'show_event') {
            if ($event->restore($q->param('event_id'))) {
                my $number_attending = 0;
                my $number_undecided = 0;
                my $number_notcoming = 0;
                $person->restore_all('category ASC, full_name ASC');
                my %temp_hash = ();
                my @undecideds = ();
                my @notcoming = ();
                while ($person->restore_next()) {
                    next if ($person->inactive() && # boolean flag for inactivity
                             ($person->is_committed($event) != 1)); # Show if committed!
                    if ($person->is_committed($event) == 1) {
                        if ($temp_hash{$person->category()}) {
                            $temp_hash{$person->category()} .= ":";
                        }
                        $temp_hash{$person->category()} .= $person->full_name();
                        $number_attending++;
                    } elsif ($person->is_committed($event) == 0) {
                        push @undecideds, $person->full_name();
                        $number_undecided++;
                    } else {
                        push @notcoming, $person->full_name();
                        $number_notcoming++;
                    }
                }

                print $q->h4("$number_attending people coming to event ".
                    "\"".$event->description()."\"".
                    ($event->location() ? (" (at ".$event->location().")") : "").
                    " on ".time_display($event->event_time()).
                    " (arrive by ".time_display($event->arrive_by(), 2). "):"), $q->start_ul();
                foreach my $cat (sort keys %temp_hash) {
                    print $q->p(), $q->li($q->h3($cat)), $q->start_ol();
                    foreach my $name (split(/:/, $temp_hash{$cat})) {
                        print $q->li($name);
                    }
                    print $q->end_ol();
                }
                print $q->end_ul(), $q->p();
                if ($number_undecided) {
                    print $q->p(), $q->hr(), $q->p();
                    print $q->h4("$number_undecided undecided people:"), $q->p();
                    my @sorted = sort(@undecideds);
                    print $q->ol($q->li(\@sorted));
                }
                if ($number_notcoming) {
                    print $q->p(), $q->hr(), $q->p();
                    print $q->h4("$number_notcoming not coming:"), $q->p();
                    my @sorted = sort(@notcoming);
                    print $q->ol($q->li(\@sorted));
                }
                my $extra_url = $has_cookie ? "" :
                    "login=".$q->param('login').";"."password=".$q->param('password');
                my $home = $q->url(-relative=>1)."?mode=begin;".$extra_url;
                my $login_screen = $q->url(-relative=>1)."?mode=login;ignore_cookie=1";
                my $prefs = $q->url(-relative=>1)."?mode=prefs;".$extra_url;
                print $q->p(), $q->start_center(), $q->start_table({-border=>1}); 
                print $q->Tr($q->td([
                    $q->a({-href=>"$prefs"}, "Login Preferences"),
                    "&nbsp;" x 20,
                    $q->a({-href=>"$home"}, "Personal Summary"),
                    "&nbsp;" x 20,
                    $q->a({-href=>"$login_screen"}, "Login Again")
                ])), $q->end_table(), $q->end_center();
                print $q->p();
                my $config = new MyConfig("/home/kayvan/public_html/afg/commitment/save/config.db", "|");
                print $q->p(), $q->start_center(), $q->start_table({-border=>1});
                my @navbar_links = ();
                my @tmp;
                $config->restore_where('key =~ /^navbar_url/', 'key ASC');
                while ($config->restore_next()) {
                    @tmp = split('\*', $config->val()); # Description*URL
                    if ($#tmp == 1) {
                        push(@navbar_links, $q->a({-href=>$tmp[1]}, $tmp[0]));
                    } else {
                        push(@navbar_links, "BAD LINK: ", $config->val());
                    }
                }
                print $q->Tr($q->td([@navbar_links]));
                print $q->end_table(), $q->end_center();
            } else { 
                print $q->h2("No such event. Maybe it was deleted."); 
            }
        } 
        if ($mode eq 'prefs') {
            $q->param('mode', 'set_prefs');
            print $q->start_form(), $q->start_center(), $q->start_table();
            print $q->Tr(
                $q->th("Enter new password: "),
                $q->td($q->password_field(-name=>'password_set', -size=>20, -maxlength=>20))
            );
            print $q->Tr( 
                $q->th("Re-enter password to confirm: "),
                $q->td($q->password_field(-name=>'password_set_confirm', -size=>20, -maxlength=>20))
            );
            my $temp_person = new Person("/home/kayvan/public_html/afg/commitment/save/persons.db", "|");
            my @cat_list = ();
            my $temp_cat;
            $temp_person->restore_all('category ASC');
            while ($temp_person->restore_next()) {
                $temp_cat = $temp_person->category();
                next if (!defined($temp_cat));
                next if grep(/$temp_cat/, @cat_list);
                push @cat_list, $temp_cat;
            }
            print $q->Tr(
                $q->th("Category: "),
                $q->td($q->popup_menu(-name=>'set_category', -values=>\@cat_list,
                    -default=>$person->category()))
            );
            my $inactive_string = 'Active' if ($person->inactive() == 0);
            $inactive_string = 'Listed but inactive' if ($person->inactive() == 1);
            $inactive_string = 'Inactive and unlisted' if ($person->inactive() > 1);
            print $q->Tr(
                $q->th("Status: "), 
                $q->td($q->popup_menu(-name=>'set_inactive',
                    -values=>['Active', 'Listed but inactive', 'Inactive and unlisted'],
                    -default=>$inactive_string))
            );
            print $q->Tr(
                $q->th("Email: "), 
                $q->td($q->textfield(-name=>'set_email', -default=>$person->email()))
            );
            print $q->Tr(
                $q->th("Street Address: "), 
                $q->td($q->textfield(-name=>'set_address', -default=>$person->address()))
            );
            print $q->Tr(
                $q->th("City: "), 
                $q->td($q->textfield(-name=>'set_city', -default=>$person->city()))
            );
            print $q->Tr(
                $q->th("State: "), 
                $q->td($q->textfield(-name=>'set_state', -default=>$person->state()))
            );
            print $q->Tr(
                $q->th("ZIP Code: "), 
                $q->td($q->textfield(-name=>'set_zip', -default=>$person->zip()))
            );
            print $q->Tr(
                $q->th("Home Phone: "), 
                $q->td($q->textfield(-name=>'set_home_phone', -default=>$person->home_phone()))
            );
            print $q->Tr(
                $q->th("Work Phone: "), 
                $q->td($q->textfield(-name=>'set_work_phone', -default=>$person->work_phone()))
            );
            print $q->Tr(
                $q->th("Fax Phone: "), 
                $q->td($q->textfield(-name=>'set_fax_phone', -default=>$person->fax_phone()))
            );
            print $q->Tr(
                $q->th("Cell Phone: "), 
                $q->td($q->textfield(-name=>'set_cell_phone', -default=>$person->cell_phone()))
            );
            print $q->Tr(
                $q->th("Wedding Anniversary: "), 
                $q->td($q->textfield(-name=>'set_anniversary', -default=>$person->anniversary()))
            );
            print $q->Tr(
                $q->th("Birthday: "), 
                $q->td($q->textfield(-name=>'set_birthday', -default=>$person->birthday()))
            );
            print $q->Tr(
                $q->th("Notes: "), 
                $q->td($q->textarea(-name=>'set_notes', -default=>$person->notes(),
                                    -rows=>3, -columns=>40))
            );
            print $q->end_table(), $q->p();
            print $q->submit(-name=>'Submit Change', -value=>'Submit Change'),
                $q->hidden(-name=>'mode', -default=>'set_prefs'),
                $q->hidden(-name=>'login', -default=>$q->param('login')),
                $q->hidden(-name=>'password', -default=>$q->param('password')),
                $q->end_center(), $q->end_form();

            my $extra_url = $has_cookie ? "" :
                "login=".$q->param('login').";"."password=".$q->param('password');
            my $home = $q->url(-relative=>1)."?mode=begin;".$extra_url;
            my $login_screen = $q->url(-relative=>1)."?mode=login;ignore_cookie=1";
            my $prefs = $q->url(-relative=>1)."?mode=prefs;".$extra_url;
            print $q->p(), $q->start_center(), $q->start_table({-border=>1}); 
            print $q->Tr($q->td([
                $q->a({-href=>"$prefs"}, "Login Preferences"),
                "&nbsp;" x 20,
                $q->a({-href=>"$home"}, "Personal Summary"),
                "&nbsp;" x 20,
                $q->a({-href=>"$login_screen"}, "Login Again")
            ])), $q->end_table(), $q->end_center();
            print $q->p();
            my $config = new MyConfig("/home/kayvan/public_html/afg/commitment/save/config.db", "|");
            print $q->p(), $q->start_center(), $q->start_table({-border=>1});
            my @navbar_links = ();
            my @tmp;
            $config->restore_where('key =~ /^navbar_url/', 'key ASC');
            while ($config->restore_next()) {
                @tmp = split('\*', $config->val()); # Description*URL
                if ($#tmp == 1) {
                    push(@navbar_links, $q->a({-href=>$tmp[1]}, $tmp[0]));
                } else {
                    push(@navbar_links, "BAD LINK: ", $config->val());
                }
            }
            print $q->Tr($q->td([@navbar_links]));
            print $q->end_table(), $q->end_center();
        }
        if ($mode eq 'set_prefs') {
            my $some_change = 0;
            if ($q->param('password_set')) {
                if ($q->param('password_set') eq $q->param('password_set_confirm')) {
                    $person->passwd($q->param('password_set')); 
                    $person->save();
                    $q->param('password', $q->param('password_set'));
                    print $q->h3("New password saved."), $q->p();
                    $some_change = 1;
                } else {
                    print $q->h3("Password entries did not match. Try again.");
                }
            }
            if ($q->param('set_category') &&
                ($q->param('set_category') ne $person->category())) {
                $person->category($q->param('set_category'));
                $person->save();
                print $q->h3("Your new category is ".$person->category().".");
                $some_change = 1;
            }
            my $new_inactive_value = 0 if ($q->param('set_inactive') eq 'Active');
            $new_inactive_value = 1 if ($q->param('set_inactive') eq 'Listed but inactive');
            $new_inactive_value = 2 if ($q->param('set_inactive') eq 'Inactive and unlisted');
            if ($q->param('set_inactive') &&
                ($person->inactive() != $new_inactive_value )) {
                $person->inactive($new_inactive_value);
                $person->save();
                if ($person->inactive() > 1) {
                    print $q->h3("You are now marked as inactive and unlisted.");
                } elsif ($person->inactive()) {
                    print $q->h3("You are now marked as inactive (but listed on the address page).");
                } else {
                    print $q->h3("You have successfully reactivated yourself.");
                }
                $some_change = 1;
            }
            if ($q->param('set_email') &&
                    ($q->param('set_email') ne $person->email())) {
                $person->email($q->param('set_email'));
                $person->save();
                print $q->h3("Your new Email is ".$person->email().".");
                $some_change = 1;
            }
            if ($q->param('set_address') &&
                    ($q->param('set_address') ne $person->address())) {
                $person->address($q->param('set_address'));
                $person->save();
                print $q->h3("Your new Street Address is ".$person->address().".");
                $some_change = 1;
            }
            if ($q->param('set_city') &&
                    ($q->param('set_city') ne $person->city())) {
                $person->city($q->param('set_city'));
                $person->save();
                print $q->h3("Your new city is ".$person->city().".");
                $some_change = 1;
            }
            if ($q->param('set_state') &&
                    ($q->param('set_state') ne $person->state())) {
                $person->state($q->param('set_state'));
                $person->save();
                print $q->h3("Your new state is ".$person->state().".");
                $some_change = 1;
            }
            if ($q->param('set_zip') &&
                    ($q->param('set_zip') ne $person->zip())) {
                $person->zip($q->param('set_zip'));
                $person->save();
                print $q->h3("Your new zip is ".$person->zip().".");
                $some_change = 1;
            }
            if ($q->param('set_home_phone') &&
                    ($q->param('set_home_phone') ne $person->home_phone())) {
                $person->home_phone($q->param('set_home_phone'));
                $person->save();
                print $q->h3("Your new home phone is ".$person->home_phone().".");
                $some_change = 1;
            }
            if ($q->param('set_work_phone') &&
                    ($q->param('set_work_phone') ne $person->work_phone())) {
                $person->work_phone($q->param('set_work_phone'));
                $person->save();
                print $q->h3("Your new work phone is ".$person->work_phone().".");
                $some_change = 1;
            }
            if ($q->param('set_fax_phone') &&
                    ($q->param('set_fax_phone') ne $person->fax_phone())) {
                $person->fax_phone($q->param('set_fax_phone'));
                $person->save();
                print $q->h3("Your new FAX phone is ".$person->fax_phone().".");
                $some_change = 1;
            }
            if ($q->param('set_cell_phone') &&
                    ($q->param('set_cell_phone') ne $person->cell_phone())) {
                $person->cell_phone($q->param('set_cell_phone'));
                $person->save();
                print $q->h3("Your new cell phone is ".$person->cell_phone().".");
                $some_change = 1;
            }
            if ($q->param('set_anniversary') &&
                    ($q->param('set_anniversary') ne $person->anniversary())) {
                $person->anniversary($q->param('set_anniversary'));
                $person->save();
                print $q->h3("Your anniversary is ".$person->anniversary().".");
                $some_change = 1;
            }
            if ($q->param('set_birthday') &&
                    ($q->param('set_birthday') ne $person->birthday())) {
                $person->birthday($q->param('set_birthday'));
                $person->save();
                print $q->h3("Your birthday is ".$person->birthday().".");
                $some_change = 1;
            }
            if ($q->param('set_notes') &&
                    ($q->param('set_notes') ne $person->notes())) {
                $person->notes($q->param('set_notes'));
                $person->save();
                print $q->h3("Your notes: ");
                print $q->pre($person->notes());
                $some_change = 1;
            }
            if (! $some_change) {
                print $q->h3("No change.");
            }
            my $extra_url = $has_cookie ? "" :
                "login=".$q->param('login').";"."password=".$q->param('password');
            my $home = $q->url(-relative=>1)."?mode=begin;".$extra_url;
            my $login_screen = $q->url(-relative=>1)."?mode=login;ignore_cookie=1";
            my $prefs = $q->url(-relative=>1)."?mode=prefs;".$extra_url;
            print $q->p(), $q->start_center(), $q->start_table({-border=>1}); 
            print $q->Tr($q->td([
                $q->a({-href=>"$prefs"}, "Login Preferences"),
                "&nbsp;" x 20,
                $q->a({-href=>"$home"}, "Personal Summary"),
                "&nbsp;" x 20,
                $q->a({-href=>"$login_screen"}, "Login Again")
            ])), $q->end_table(), $q->end_center();
            print $q->p();
            my $config = new MyConfig("/home/kayvan/public_html/afg/commitment/save/config.db", "|");
            print $q->p(), $q->start_center(), $q->start_table({-border=>1});
            my @navbar_links = ();
            my @tmp;
            $config->restore_where('key =~ /^navbar_url/', 'key ASC');
            while ($config->restore_next()) {
                @tmp = split('\*', $config->val()); # Description*URL
                if ($#tmp == 1) {
                    push(@navbar_links, $q->a({-href=>$tmp[1]}, $tmp[0]));
                } else {
                    push(@navbar_links, "BAD LINK: ", $config->val());
                }
            }
            print $q->Tr($q->td([@navbar_links]));
            print $q->end_table(), $q->end_center();
        }
    } else {
        %cookie_values = ( session_id => 0 );
        my $cookie = $q->cookie(-name => 'commitme',
            -value=>\%cookie_values, -expires=>'+21d');
        print $q->header(-cookie=>$cookie),
            $q->start_html(-title=>'CommitMe', -bgcolor=>'#FFFFFF'),
            $q->center($q->h1('CommitMe!')), $q->hr();
        print $q->h1('Bad Login or Password'), $q->p(),
            "Hit your bowser BACK button and try again.";
    }
}
print $q->p(), $q->hr();
print $q->i("Page generated on " . localtime() .
    ". To report problems, send mail to ".
    $q->a({href=>"mailto:kayvansylvan\@gmail.com"},
    "Kayvan Sylvan"));
print $q->end_html(); 
