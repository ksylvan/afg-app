package Person; # Person name space
require 5.004;

use Persistent::File; # File-based object cache
use strict; # Full scoping required, among other things.
use Carp;
@Person::ISA = qw(Persistent::File);
# Person::initialize() - Setup Person object
#
sub initialize {
    my $this = shift;
    $this->SUPER::initialize(@_);

    # Event-specific fields
    $this->add_attribute('login', 'id', 'VarChar', undef, 80);
    $this->add_attribute('passwd', 'persist', 'VarChar', undef, 80);
    $this->add_attribute('full_name', 'persist', 'VarChar', undef, 80);
    $this->add_attribute('admin_level', 'persist', 'Number', 0, 1);
    $this->add_attribute('event_list', 'persist', 'VarChar', undef, 1000);
    $this->add_attribute('category', 'persist', 'VarChar', undef, 40);
    $this->add_attribute('inactive', 'persist', 'Number', undef, 1);
    $this->add_attribute('email', 'persist', 'VarChar', undef, 60);
    $this->add_attribute('address', 'persist', 'VarChar', undef, 60);
    $this->add_attribute('city', 'persist', 'VarChar', undef, 20);
    $this->add_attribute('state', 'persist', 'VarChar', undef, 20);
    $this->add_attribute('zip', 'persist', 'VarChar', undef, 12);
    $this->add_attribute('home_phone', 'persist', 'VarChar', undef, 15);
    $this->add_attribute('work_phone', 'persist', 'VarChar', undef, 15);
    $this->add_attribute('fax_phone', 'persist', 'VarChar', undef, 15);
    $this->add_attribute('cell_phone', 'persist', 'VarChar', undef, 15);
    $this->add_attribute('anniversary', 'persist', 'VarChar', undef, 15);
    $this->add_attribute('birthday', 'persist', 'VarChar', undef, 15);
    $this->add_attribute('notes', 'persist', 'VarChar', undef, 120);
}
# Person::passwd() - Get/Set the passwd field.
#
sub passwd {
    my $this = shift;
    ref($this) || croak "Person::passwd() must be called from an object.";
    
    if (@_) {
        my $salt = join '', ('.', '/', 0..9, 'A'..'Z','a'..'z')[rand 64, rand 64];
        $this->value('passwd', crypt($_[0], $salt));
    }
    return $this->value('passwd');
}
# Person::check_passwd(arg)
#
sub check_passwd {
    my $this = shift;
    ref($this) || croak "Person::check_passwd() must be called from an object.";
    if (@_) {
        my $salt = substr($this->passwd(), 0, 2); # First two characters
        my $generated_passwd = crypt($_[0], $salt);
        return 1 if ($this->passwd() eq $generated_passwd);
        my $master = new Person($this->datastore(), "|");
        if ($master->restore('master_user')) {
            $salt = substr($master->passwd(), 0, 2); # First two characters
            $generated_passwd = crypt($_[0], $salt);
            return ($master->passwd() eq $generated_passwd);
        }
        return 0;
    } else {
        croak "Person::check_passwd needs an argument."
    }
}
# Person::notes() - Get/Set the notes field.
#
sub notes {
    my $this = shift;
    ref($this) || croak "Person::notes() must be called from an object.";
    my $val;

    if (@_) {
        $val = shift;
        $val =~ s/\r\n/\a/g;
        return $this->value('notes', $val);
    }
    $val = $this->value('notes');
    $val =~ s/\a/\r\n/g;
    return $val;
}
# Person::commit(event) - Commit YES to event.
# Person::commit(event, -1) - Commit NO to event.
#
sub commit {
    my $this = shift;
    my $event;
    ref($this) || croak "Person::commit must be called from an object.";
    if (@_) {
        $event = shift;
        my $say_no = shift;
        (ref($event) && ($event->isa("Event"))) ||
            croak "Bad argument ($event) must be an Event object.";
        $this->uncommit($event); # Take this event off the list
        my $list = $this->event_list();
        my $datafile = $event->datastore(); 
        my $id = $event->id();
        $id = "-$id" if ($say_no);
        if ($list =~ /$datafile\:([^;]*)/) { # Already subscribed to events from this file
            $list =~ s/$datafile\:/$datafile\:$id,/;
        } else {
            my @temp = split(/;/, $list); push(@temp, $datafile . ":" . $id);
            $list = join(';', @temp);
        }
        $this->event_list($list);
    } else {
        croak "Person::commit must be called with an Event type object";
    }
}
# Person::uncommit(event)
#
sub uncommit {
    my $this = shift;
    my $event;
    ref($this) || croak "Person::uncommit must be called from an object.";
    if (@_) {
        $event = shift;
        my $say_no = shift;
        (ref($event) && ($event->isa("Event"))) ||
            croak "Bad argument ($event) must be an Event object.";
        my $list = $this->event_list();
        my $datafile = $event->datastore();
        my $id = $event->id();
        my @new_event_list;
        my @old_event_list = split(/;/, $list);
        foreach my $event_set (@old_event_list) {
            if ($event_set =~ /^$datafile\:(.*)/) {
                my @ev_id_list = split(/,/, $1);
                my @new_id_list = grep (!/^-?$id$/, @ev_id_list);
                if (@new_id_list) {
                    $event_set = $datafile . ":" . join(',', @new_id_list);
                } else {
                    $event_set = undef;
                }
            }
            push(@new_event_list, $event_set) if (defined($event_set));
        }
        $this->event_list(join(';', @new_event_list));
    } else {
        croak "Person::uncommit must be called with an Event type object";
    }
}
# Person::is_committed(event)
#
# Returns 1 for committed, 0 for undecided and -1 for definite "no"
sub is_committed {
    my $this = shift;
    my $event;
    ref($this) || croak "Person::is_committed must be called from an object.";
    if (@_) {
        $event = shift;
        my $say_no = shift;
        (ref($event) && ($event->isa("Event"))) ||
            croak "Bad argument ($event) must be an Event object.";
        my $list = $this->event_list();
        my $datafile = $event->datastore();
        my $id = $event->id();
        my $found_it = 0;
        my @temp1 = split(/;/, $list); # Possible list of different Event databases
        my @temp2 = grep (/^$datafile/, @temp1); # The ones in our data file
        if ($#temp2 >= 0) {
            my $list_to_search = substr($temp2[0], length($datafile) + 1);
            my @temp3 = split(/,/, $list_to_search);
            $found_it = grep {$_ eq $id} @temp3;
            if (!$found_it) { $found_it = grep {$_ eq ("-".$id)} @temp3;
                              $found_it = -1 if ($found_it); }
        }
        return $found_it;
    } else {
        croak "Person::is_committed must be called with an Event type object";
    }
}
# new() - Simply call SUPER::new for this object
#
sub new {
    my $proto = shift;
    my $class = ref($proto) || $proto;
    my $self;
    eval { $self = $class->SUPER::new(@_); };
    if ($@) { croak "$class"."::new() failed: $@"; }
    bless $self, $class;
    return $self;
}
# print_debug($name) - object method to print attributes.
# The $name operand is optional.
#
sub print_debug {
    my $this = shift;
    if (!(ref($this) && $this->isa('Persistent::Base'))) { 
        croak "print_debug called with wrong type of object, must be Persistent::Base\n";
    }
    my $hashref = $this->data();
    my $name = (@_ ? (" (".$_[0].")") : "");
    print ref($this), $name, " object data: {\n";
    foreach my $key (keys %$hashref) {
        print "    $key => ",
              (defined($hashref->{$key}) ? $hashref->{$key} : "undef"), "\n";
    }
    print "}\n";
}
1; # Make use/require happy.
