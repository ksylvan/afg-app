#!/usr/bin/perl
#
# unit-test of the Event.pm module.
#
# Author: Kayvan Sylvan
#
use lib "/home/kayvan/public_html/afg/commitment/modules";
use lib "/home/kayvan/perl5/lib/perl5";

use Event;
use strict;

my $tmpname = "/var/tmp/testev$$";
my $ev1 = new Event($tmpname, "|"); # File delimiter is the vertical bar
$ev1->description("AFG Movie Outing");
$ev1->event_time("2000-07-15 13:00:00");
$ev1->arrive_by("2000-07-15 12:30:00");
$ev1->save(); # Save this for later.
my $ev2 = new Event($tmpname, "|");
$ev2->description("AFG Campout");
$ev2->event_time("2000-08-15 13:00:00");
$ev2->arrive_by("2000-08-15 12:30:00");
$ev2->save();
$ev1->print_debug("ev1");
$ev2->print_debug("ev2");
my $ev3 = new Event($tmpname, "|");
print "File $tmpname contains ", $ev3->restore_all(), " events.\n";
while ($ev3->restore_next()) {
    $ev3->print_debug("ev3");
}
# Remove the object cache and lock file
unlink($tmpname); unlink($tmpname.".lock");
print "$tmpname removed.\n";
