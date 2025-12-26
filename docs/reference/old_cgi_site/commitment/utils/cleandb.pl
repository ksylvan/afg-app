#!/usr/bin/perl
#
# Event and Person database maintenance
#
# Author: Kayvan Sylvan
#
use lib "/home/kayvan/public_html/afg/commitment/modules";
use lib "/home/kayvan/perl5/lib/perl5";
use Person;
use Event;
use strict;

use Getopt::Std;
my %opts;
getopts('p:e:h?', \%opts);
my $persondb = $opts{p} ? $opts{p} : "/home/kayvan/public_html/afg/commitment/save/persons.db";
my $eventsdb = $opts{e} ? $opts{e} : "/home/kayvan/public_html/afg/commitment/save/events.db";
if (defined($opts{h} || $opts{'?'})) {
    print "Usage: cleandb.pl [-p persondb] [-e eventdb] | -h | -?\n";
    print "Default person database: /home/kayvan/public_html/afg/commitment/save/persons.db\n";
    print "Default event database: /home/kayvan/public_html/afg/commitment/save/events.db\n";
    exit;
}
my $person = new Person($persondb, '|');
my $event = new Event($eventsdb, '|');
my $now_date_time = new Persistent::DataType::DateTime('now');
my $now_time = $now_date_time->value(); # Get the string
my @expired_events = ();
$event->restore_all('event_time ASC'); # Sort the events by date!
while ($event->restore_next()) {
    last if ($now_time le $event->event_time());
    $event->delete();
}
$person->restore_all();
while ($person->restore_next()) {
    my $list = $person->event_list();
    my @file_list = split(';', $list);
    my @new_file_list = ();
    foreach my $l (@file_list) {
        my @x = split(':', $l);
        my $file = $x[0];
        my $ev_list = $x[1];
        my @ev = split(',', $ev_list);
        my $e = new Event($file, '|');
        my @new_ev = ();
        foreach my $ev_id (@ev) {
            if ($ev_id =~ /^-(.*)$/) {
                if ($e->restore($1)) { push @new_ev, $ev_id; }
            } else {
                if ($e->restore($ev_id)) { push @new_ev, $ev_id; }
            }
        }
        push @new_file_list, $file.':'.join(',', @new_ev);
    }
    $person->event_list(join(';', @new_file_list));
    $person->save();
}
