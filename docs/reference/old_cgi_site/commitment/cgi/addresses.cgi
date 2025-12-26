#!/usr/bin/perl
#
# Show Name and Address list.
#
# Author: Kayvan Sylvan
#
use lib "/home/kayvan/perl5/lib/perl5";
use lib "/home/kayvan/public_html/afg/commitment/modules";
use lib "/home/kayvan/perl/local/lib/perl5/site_perl/5.10.0";
use Person;
use CGI qw(-debug -no_xhtml); # Perl CGI scripting.
use CGI::Carp 'fatalsToBrowser'; # Report errors to browser, not just server log
use strict;

my $q = new CGI; # The query object
my $person = new Person("/home/kayvan/public_html/afg/commitment/save/persons.db", "|");
use MyConfig;

my $config = new MyConfig("/home/kayvan/public_html/afg/commitment/save/config.db", "|");
if (!$config->restore('address_list_header')) {
    $config->key('address_list_header');
    $config->val('Name and Address List');
    $config->save(); # Save default
}
my %cookie_values = $q->cookie('commitme');
my $has_cookie = defined($q->cookie('commitme'));
my $cookie = $q->cookie(-name => 'commitme',
    -value=>\%cookie_values, -expires=>'+21d');
if ($has_cookie) {
  print $q->header(-cookie => $cookie);
} else {
  print $q->header();
}
print $q->start_html(-title=>$config->val(), -bgcolor=>'#FFFFFF'),
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
if ($has_cookie) {
  print $q->p();
  $person->restore_all('full_name ASC'); # Sort the people!
  print $q->start_center(), $q->start_table({-border=>1});
  print $q->Tr($q->th("Name & Address"), $q->th("Phones"),
      $q->th("Anniversary"), $q->th("Birthday"), $q->th("Notes")); 
  while ($person->restore_next()) {
      next if ($person->inactive() > 1);
      my $email = $person->email();
      my $address = $q->start_table({border=>0});
      $address .= $q->Tr($q->td($q->b($person->full_name())));
      if ($person->address()) {
          $address .= $q->Tr($q->td($person->address()));
          $address .= $q->Tr($q->td($person->city().", ".
                                    $person->state()." ".$person->zip()));
      }
      $address .= $q->Tr($q->td($email ?
                                $q->a({href=>"mailto:$email"}, $email) :
                                $q->i('No Email')));
      $address .= $q->end_table();
      my $phone = $q->start_table({border=>0});
      my $pparts;
      $pparts .= $q->Tr($q->td("H: ".$person->home_phone())) if $person->home_phone();
      $pparts .= $q->Tr($q->td("W: ". $person->work_phone())) if $person->work_phone();
      $pparts .= $q->Tr($q->td("Fax: ".$person->fax_phone())) if $person->fax_phone();
      $pparts .= $q->Tr($q->td("Cell: ".$person->cell_phone())) if $person->cell_phone();
      $pparts = '&nbsp;' if (!defined($pparts));
      $phone .= $pparts;
      $phone .= $q->end_table();

      my $anniv = $person->anniversary();
      $anniv = '&nbsp;' if !defined($anniv);

      my $bday = $person->birthday();
      $bday = '&nbsp;' if !defined($bday);

      my $notes = $person->notes();
      $notes =~ s/\r\n/<BR>/g;
      $notes = '&nbsp;' if !defined($notes);

      print $q->Tr({-valign=>'CENTER', halign=>'CENTER'},
          $q->td($address), $q->td($phone),
          $q->td($anniv), $q->td($bday), $q->td($notes));
  }
  print $q->end_table(), $q->end_center(), $q->p();
} else {
  print $q->center($q->h3("Not authorized to see the address list. Login first."));
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
