#!/usr/bin/perl
#
# Event database maintenance.
#
# Author: Kayvan Sylvan
#
use lib "/home/kayvan/public_html/afg/commitment/modules";
use lib "/home/kayvan/perl5/lib/perl5";
use Event;
use strict;
my %help;
my $help_summary = "help => Print command list or help for a command\n";
$help{help} = "help command => Print command-specific help\n";
$help{help} .= "help => Print the general help message\n";
$help_summary .= "quit => Quit the eventdb.pl utility\n";
$help{quit} = "quit => Quit the application\n";
$help_summary .= "add => Add an event to the database\n";
$help{add} = "add \"Description of event\" {time-of-event} {time-to-arrive}\n";
$help{add} .= "add \"Description of event\" {time-of-event} -{minutes-before}\n";
$help{add} .= "The time-to-arrive and time-of-event are like YYYY-MM-DD hh:mm:ss\n";
$help{add} .= "The minutes-before is an integer.\n";
$help_summary .= "list => List all events in database\n";
$help{list} = "list=> List all events in database\n";
$help_summary .= "delete => Delete events in database\n";
$help{delete} = "delete number => Delete the event with id {number} from database\n";
$help_summary .= "modify => Modify events in database\n";
$help{modify} = "modify number \"Description\" => Change description of event\n";
$help{modify} .= "modify number YYYY-MM-DD hh:mm:ss => Change time for event\n";
$help{modify} .= "modify number -{number-of-minutes} => Change arrival time.\n";
$help{modify} .= "modify number @\"Location\" => Change location.\n";

# eventdb_command(dbfile, FILEHANDLE, command-string)
#
sub eventdb_command {
    my ($dbfile, $FILE, $cmd) = @_;
    $_ = $cmd;
    # Help string output.
    if (/^help$/) { print $FILE $help_summary; return; }
    if (/^help\s+(\S+)/) {
        if (defined($help{$1})) {
            print $FILE $help{$1};
        } else {
            print $FILE "No help string for command \"$1\"\n";
        }
        return;
    }
    # Quit command
    if (/^quit$/ || /^quit\s/) { print $FILE "Goodbye!\n"; exit; }
    # Add command
    if (/^add\s+"([^"]+)"\s+(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s*$/) {
        my $event = new Event($dbfile, "|");
        $event->description($1);
        $event->event_time($2);
        $event->arrive_by($3);
        eval { $event->save(); };
        if ($@) { print $FILE $@; }
        else {
            print $FILE "Added event \"$1\" (at $2, arrive at $3) to $dbfile\n";
        }
        return; 
    } 
    # Add command
    if (/^add\s+"([^"]+)"\s+(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+-(\d+)\s*$/) {
        my $event = new Event($dbfile, "|");
        my @arrive_by;
        $event->description($1);
        $event->event_time($2);
        my $minutes_early = $3;
        use Time::Local;
        my $evt = new Persistent::DataType::DateTime($event->event_time());
        my $ts = timelocal($evt->seconds(), $evt->minutes(), $evt->hours(),
            $evt->day(), $evt->month() - 1, $evt->year() - 1900);
        $ts -= ($minutes_early * 60);
        @arrive_by = localtime($ts);
        $event->arrive_by(@arrive_by);
        eval { $event->save(); };
        if ($@) { print $FILE $@; }
        else {
            print $FILE "Added event \"$1\" (at $2, arrive at ",
                $event->arrive_by(), ") to $dbfile\n";
        }
        return; 
    } 
    # Add command syntax error
    if (/^add$/ || /^add\s/) {
        print $FILE "Add: Syntax error!\n";
        print $FILE $help{add};
        return;
    }
    if (/^list/) {
        my $event = new Event($dbfile, "|");
        $event->restore_all('event_time ASC');
        while ($event->restore_next()) {
            print $FILE $event->id(), " => ", $event->description(),
                ($event->location() ? " (At ".$event->location().") " : " "),
                $event->event_time(), ", arrive by ", $event->arrive_by(), ")\n";
        }
        return;
    }
    if (/^delete\s+(\d+)\s*$/) {
        my $event = new Event($dbfile, "|");
        if ($event->restore($1)) {
            eval { $event->delete(); };
            if ($@) {
                print $FILE "Deletion of event $1 failed: $@";
            } else {
                print $FILE "Event $1 (", $event->description(), ") deleted.\n";
            };
        } else {
            print $FILE "No event ($1) in $dbfile\n";
        }
        return;
    }
    if (/^delete$/ || /^delete\s/) {
        print $FILE "delete: syntax error!\n";
        print $FILE $help{delete};
        return;
    }
    if (/^modify\s+(\d+)\s+"([^"]+)"\s*$/) {
        my $event = new Event($dbfile, "|");
        if ($event->restore($1)) {
            $event->description($2);
            eval { $event->save(); };
            if ($@) {
                print $FILE "Update of event $1 failed: $@";
            } else {
                print $FILE "Event $1 (", $event->description(), ") saved.\n";
            };
        } else {
            print $FILE "No event ($1) in $dbfile\n";
        }
        return;
    }
    if (/^modify\s+(\d+)\s+(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s*$/) {
        my $event = new Event($dbfile, "|");
        if ($event->restore($1)) {
            $event->event_time($2);
            eval { $event->save(); };
            if ($@) {
                print $FILE "Update of event $1 failed: $@";
            } else {
                print $FILE "Event $1 (", $event->description(), ") saved.\n";
            };
        } else {
            print $FILE "No event ($1) in $dbfile\n";
        }
        return;
    }
    if (/^modify\s+(\d+)\s+-(\d+)\s*$/) {
        my $event = new Event($dbfile, "|");
        if ($event->restore($1)) {
            my $minutes_early = $2;
            my @arrive_by;
            use Time::Local;
            my $evt = new Persistent::DataType::DateTime($event->event_time());
            my $ts = timelocal($evt->seconds(), $evt->minutes(), $evt->hours(),
                $evt->day(), $evt->month() - 1, $evt->year() - 1900);
            $ts -= ($minutes_early * 60);
            @arrive_by = localtime($ts);
            $event->arrive_by(@arrive_by);
            eval { $event->save(); };
            if ($@) {
                print $FILE "Update of event $1 failed: $@";
            } else {
                print $FILE "Event $1 (", $event->description(), ") saved.\n";
            };
        } else {
            print $FILE "No event ($1) in $dbfile\n";
        }
        return;
    }
    if (/^modify\s+(\d+)\s+\@\"(.+)\"$/) {
        my $event = new Event($dbfile, "|");
        if ($event->restore($1)) {
            my $location = $2;
            $event->location($location);
            eval { $event->save(); };
            if ($@) {
                print $FILE "Update of event $1 failed: $@";
            } else {
                print $FILE "Event $1 (", $event->description(), ") saved.\n";
            };
        } else {
            print $FILE "No event ($1) in $dbfile\n";
        }
        return;
    }
    if (/^modify$/ || /^modify\s/) {
        print $FILE "modify: syntax error!\n";
        print $FILE $help{modify};
        return;
    }
    print $FILE "Unknown command: $cmd\n";
}
use Getopt::Std;
my %opts;
getopts('f:ch?', \%opts);
my $filename = $opts{f} ? $opts{f} : "/home/kayvan/public_html/afg/commitment/save/events.db";
if (defined($opts{'?'}) || defined($opts{'h'})) {
    print "Usage: eventdb.pl [-f file] [-h] [-?] [-c {commands}]\n\n";
    print "Options:\n";
    print "  -f file => Choose file to edit.\n";
    print "  -h or -? => Print this help screen and exit.\n";
    print "  -c => Take the rest of the arguments as eventdb commands.\n\n";
    print "The default file is /home/kayvan/public_html/afg/commitment/save/events.db\n";
    exit 0;
}
if (defined($opts{c})) {
    eventdb_command($filename, *STDOUT{IO}, join(" ", @ARGV));
} else {
    use Term::ReadLine;
    my $prompt = "eventdb> ";
    my $term = new Term::ReadLine 'EventDB Maintenance';
    my $OUT = $term->OUT || *STDOUT{IO};
    while (defined($_ = $term->readline($prompt))) {
        if (/\S/) {
            eventdb_command($filename, $OUT, $_);
            $term->addhistory($_);
        }
    }
    print $OUT "\n"; eventdb_command($filename, $OUT, "quit");
}
