#!/usr/bin/perl
#
# Person database maintenance.
#
# Author: Kayvan Sylvan
#
use lib "/home/kayvan/public_html/afg/commitment/modules";
use lib "/home/kayvan/perl5/lib/perl5";
use Person;
use strict;
my %help;
my $help_summary = "help => Print command list or help for a command\n";
$help{help} = "help command => Print command-specific help\n";
$help{help} .= "help => Print the general help message\n";
$help_summary .= "quit => Quit\n";
$help{quit} = "quit => Quit the persondb utility.\n";
$help_summary .= "add => To add a person\n";
$help{add} = "add => add login \"full-name\" [password].\n";
$help{add} .= "login and quoted full-name are mandatory.\n";
$help{add} .= "If the password is unspecified, we will prompt for it.\n";
$help_summary .= "delete => Delete a person\n";
$help{delete} = "delete login => Delete login from the file.\n";
$help_summary .= "modify => Modify a person\n";
$help{modify} = "modify login \"Full Name\" => Modify full-name of login.\n";
$help{modify} .= "modify login password => Modify the password.\n";
$help{modify} .= "modify login \"Full Name\" passwd => Modify both.\n";
$help_summary .= "admin => Modify the admin level\n";
$help{admin} = "admin login number => Set the admin_level of login to number\n";
$help_summary .= "inactive => Set the inactive flag\n";
$help{inactive} = "inactive login number => Set the inactive flag of login to number\n";
$help_summary .= "cat => Set up a category\n";
$help{cat} = "cat login \"category\" => Set the category for login.\n";
$help_summary .= "list => List all persons in database\n";
$help{list} = "list=> List all people in database\n";

# persondb_command(dbfile, FILEHANDLE, command-string)
#
sub persondb_command {
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
    # Quit.
    if (/^quit$/ || /^quit\s/) { print $FILE "Goodbye!\n"; exit; }
    # add - Add a person
    if (/^add\s+(\S+)\s+"([^"]+)"\s+(.*)/) {
        my $person = new Person($dbfile, "|");
        $person->login($1); $person->full_name($2); $person->passwd($3);
        eval { $person->save(); };
        if ($@) { print $FILE $@; }
        else {
            print $FILE "Added login $1 ($2) with password \"$3\" to $dbfile\n";
        }
        return;
    }
    if (/^add\s+(\S+)\s+"([^"]+)"/) {
        my $person = new Person($dbfile, "|");
        $person->login($1); $person->full_name($2);
        print $FILE "Type in password: ";
        system("stty -echo");
        my $p1 = <STDIN>; chomp($p1); print $FILE "\n";
        print $FILE "Type in password again: ";
        my $p2 = <STDIN>; chomp($p2); print $FILE "\n";
        system("stty echo");
        if ($p1 ne $p2) {
            print $FILE "Passwords do not match!\n";
            return;
        }
        $person->passwd($p1);
        eval { $person->save(); };
        if ($@) { print $FILE $@; }
        else {
            print $FILE "Added login $1 ($2) to $dbfile\n";
        }
        return;
    }
    if (/^add\s/ || /^add$/) {
        print $FILE "add: syntax error!\n";
        print $FILE $help{add};
        return;
    }
    # Delete.
    if (/^delete\s+(\S+)/) {
        my $person = new Person($dbfile, "|");
        if ($person->restore($1)) {
            eval { $person->delete(); };
            if ($@) { print $FILE $@; return; }
            else {
                print $FILE "Deletion of $1 (", $person->full_name(), ") successful.\n"; 
            }
        } else {
            print $FILE "No such login \"$1\" in $dbfile\n";
        }
        return;
    }
    if (/^delete$/ || /^delete\s/) {
        print $FILE "delete: syntax error!\n";
        print $FILE $help{delete};
        return;
    }
    # Modify.
    if (/^modify\s+(\S+)\s+"([^"]+)"/) {
        my $person = new Person($dbfile, "|");
        if ($person->restore($1)) {
            $person->full_name($2);
            eval { $person->save(); };
            if ($@) { print $FILE $@; return; }
            else {
                print $FILE "Update of $1 (", $person->full_name(), ") successful.\n"; 
            }
        } else {
            print $FILE "No such login \"$1\" in $dbfile\n";
        }
        return;
    }
    if (/^modify\s+(\S+)\s+(\S+)/) {
        my $person = new Person($dbfile, "|");
        if ($person->restore($1)) {
            $person->passwd($2);
            eval { $person->save(); };
            if ($@) { print $FILE $@; return; }
            else {
                print $FILE "Update of $1 (", $person->full_name(), ") successful.\n"; 
            }
        } else {
            print $FILE "No such login \"$1\" in $dbfile\n";
        }
        return;
    }
    if (/^modify\s+(\S+)\s+"([^"]*)\s+(\S+)/) {
        my $person = new Person($dbfile, "|");
        if ($person->restore($1)) {
            $person->full_name($2);
            $person->passwd($3);
            eval { $person->save(); };
            if ($@) { print $FILE $@; return; }
            else {
                print $FILE "Update of $1 (", $person->full_name(), ") successful.\n"; 
            }
        } else {
            print $FILE "No such login \"$1\" in $dbfile\n";
        }
        return;
    }
    if (/^modify$/ || /^modify\s/) {
        print $FILE "modify: syntax error!\n";
        print $FILE $help{modify};
        return;
    }
    if (/^admin\s+(\S+)\s+([0-9])/) {
        my $person = new Person($dbfile, "|");
        if ($person->restore($1)) {
            $person->admin_level($2);
            $person->save();
            print $FILE "Admin level for \"$1\" (", $person->full_name(),
                ") changed to ", $2, "\n";
        } else {
            print $FILE "No such login \"$1\" in $dbfile\n"; 
        }
        return;
    }
    if (/^admin$/ || /^admin\s/) {
        print $FILE "admin: Syntax error!\n";
        print $FILE $help{admin};
        return;
    }
    if (/^inactive\s+(\S+)\s+([0-9])/) {
        my $person = new Person($dbfile, "|");
        if ($person->restore($1)) {
            $person->inactive($2);
            $person->save();
            print $FILE "inactive for \"$1\" (", $person->full_name(),
                ") changed to ", $2, "\n";
        } else {
            print $FILE "No such login \"$1\" in $dbfile\n"; 
        }
        return;
    }
    if (/^inactive$/ || /^inactive\s/) {
        print $FILE "inactive: Syntax error!\n";
        print $FILE $help{inactive};
        return;
    }
    # Cat(egorize)
    if (/^cat\s+(\S+)\s+\"([^"]+)\"\s*$/) { 
        my $person = new Person($dbfile, "|");
        if ($person->restore($1)) {
            $person->category($2);
            eval { $person->save(); };
            if ($@) { print $FILE $@; return; }
            else {
                print $FILE "Update of $1 (", $person->full_name(), ") successful.\n"; 
            }
        } else {
            print $FILE "No such login \"$1\" in $dbfile\n";
        }
        return;
    }
    if (/^cat$/ || /^cat\s/) {
        print $FILE "cat: syntax error!\n";
        print $FILE $help{cat};
        return;
    }
    if (/^list/) {
        my $person = new Person($dbfile, "|");
        $person->restore_all('login ASC');
        while ($person->restore_next()) {
            print $FILE $person->login(), " => ", $person->full_name(),
                ($person->admin_level() ? " (admin) " : " (user) "), 
                ($person->category() ? $person->category() : "UNSET"), "\n";
        }
        return;
    }
    print $FILE "Unknown command: $cmd\n";
}
use Getopt::Std;
my %opts;
getopts('f:ch?', \%opts);
my $filename = $opts{f} ? $opts{f} : "/home/kayvan/public_html/afg/commitment/save/persons.db";
if (defined($opts{'?'}) || defined($opts{'h'})) {
    print "Usage: persondb.pl [-f file] [-h] [-?] [-c {commands}]\n\n";
    print "Options:\n";
    print "  -f file => Choose file to edit.\n";
    print "  -h or -? => Print this help screen and exit.\n";
    print "  -c => Take the rest of the arguments as persondb commands.\n\n";
    print "The default file is /home/kayvan/public_html/afg/commitment/save/persons.db\n";
    exit 0;
}
if (defined($opts{c})) {
    persondb_command($filename, *STDOUT{IO}, join(" ", @ARGV));
} else {
    use Term::ReadLine;
    my $prompt = "persondb> ";
    my $term = new Term::ReadLine 'PersonDB Maintenance';
    my $OUT = $term->OUT || *STDOUT{IO};
    while (defined($_ = $term->readline($prompt))) {
        if (/\S/) {
            persondb_command($filename, $OUT, $_);
            $term->addhistory($_);
        }
    }
    print $OUT "\n"; persondb_command($filename, $OUT, "quit");
}
