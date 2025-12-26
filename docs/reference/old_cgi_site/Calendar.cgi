#!/usr/bin/perl
#
# Show view of upcoming events as a calendar.
#
# Author: Kayvan Sylvan
#
use lib "/home/kayvan/perl5/lib/perl5";
use lib "/home/kayvan/public_html/afg/commitment/modules";
use lib "/home/kayvan/perl/local/lib/perl5/site_perl/5.10.0";
use Event;
use CGI qw(-debug -no_xhtml); # Perl CGI scripting.
use CGI::Carp 'fatalsToBrowser'; # Report errors to browser, not just server log
use strict;

my $q = new CGI; # The query object
my $event = new Event("/home/kayvan/public_html/afg/commitment/save/events.db", "|");
use utils;
use MyConfig;

my $config = new MyConfig("/home/kayvan/public_html/afg/commitment/save/config.db", "|");
if (!$config->restore('calendar_header')) {
    $config->key('calendar_header');
    $config->val('Upcoming Events Calendar');
    $config->save(); # Save default
}
print $q->header(), $q->start_html(-title=>$config->val(), -bgcolor=>'#FFFFFF'),
    $q->center($q->h1($config->val())), $q->hr();
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
    my $last_month = "";
    my ($this_month, $tmp_mon, $tmp_year);
    print $q->start_center();
    foreach my $event_id (@current_events) {
        next if (!$event->restore($event_id)); # Only can happen if id was deleted!
        $this_month = substr($event->event_time(), 0, 7);
        if ($last_month ne $this_month) {
            print $q->end_table() if ($last_month ne "");
            $tmp_year = substr($this_month, 0, 4);
            $tmp_mon = substr($this_month, 5, 2);
            print $q->h2(month_name($tmp_mon)." ".$tmp_year);
            print $q->start_table({-border=>undef});
            print $q->Tr({-align=>"CENTER"},
                $q->th(["Description", "Date and Time", "Arrive By"]));
            $last_month = $this_month;
        }
        my $desc = $event->description();
        if ($event->location()) { $desc .= " (At ".$event->location.")"; }
        print $q->Tr({-align=>"CENTER"},
            $q->td([$desc, time_display($event->event_time()),
                time_display($event->arrive_by(), 2)]));
    }
    print $q->end_table(), $q->end_center();
} else {
    print $q->p(), $q->p(), "There are no upcoming events, sorry!";
}
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
print $q->p(), $q->hr();
print $q->i("Page generated on " . localtime() .
    ". To report problems, send mail to ".
    $q->a({href=>"mailto:kayvansylvan\@gmail.com"},
    "Kayvan Sylvan"));
print $q->end_html();
