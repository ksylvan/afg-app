package MyConfig; # Generic Config object
require 5.004;

use Persistent::File; # File-based object cache
use strict; # Full scoping required, among other things.
use Carp;
@MyConfig::ISA = qw(Persistent::File);
# MyConfig::initialize() - Automatically called by new()
#
sub initialize {
    my $this = shift;
    $this->SUPER::initialize(@_);

    # MyConfig-specific fields
    $this->add_attribute('key', 'id', 'VarChar', undef, 20);
    $this->add_attribute('val', 'persist', 'VarChar', undef, 120);
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
