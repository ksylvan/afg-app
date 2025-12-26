package Event; # Event name space
require 5.004;

$ENV{"TZ"}="PST8PDT";
use Persistent::File; # File-based object cache
use strict; # Full scoping required, among other things.
use Carp;
@Event::ISA = qw(Persistent::File);
use Counter; # A Persistent::File counter
# Event::initialize() - Automatically called by new()
#
sub initialize {
    my $this = shift;
    $this->SUPER::initialize(@_);

    # Event-specific fields
    $this->add_attribute('id', 'id', 'Number', undef, 5, 0);
    $this->add_attribute('description', 'persist', 'VarChar', undef, 80);
    $this->add_attribute('event_time', 'persist', 'DateTime', undef);
    $this->add_attribute('arrive_by', 'persist', 'DateTime', undef);
    $this->add_attribute('location', 'persist', 'VarChar', undef, 50);
}
# Event::save() - class-specific save method
#
sub save {
    my $this = shift;
    if (!defined($this->id)) {
        my $counter = new Counter("/home/kayvan/public_html/afg/commitment/save/counter.db");
        if ($counter->restore('event')) { # exists
            $counter->val($counter->val() + 1); # increment it
        } else {
            $counter->key('event');
            $counter->val(0);
        }
        $counter->save();
        $this->id($counter->val());
    }
    $this->SUPER::save(@_);
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
