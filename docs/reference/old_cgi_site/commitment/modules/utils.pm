# time_display(time_string, format)
# Take a date-time (YYYY-MM-DD hh:mm:ss) and return a string in another format.
# format is optional (defaults to 0)
# format summary:
# 0 => MM/DD/YY hh:mm AM/PM
# 1 => MM/DD/YY hh:mm (24 hour time)
# 2 => hh:mm AM/PM (time only)
# 3 => hh:mm (24 hour time)
sub time_display {
    my ($str, $format) = @_;
    $format = 0 if (!defined($format));
    if ($str =~ /(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})/) {
        my $YY = substr($1, 2); # The last two digits of the year
        my ($ampm, $fixhr);
        if ($4 > 12) {
            $ampm = "PM"; $fixhr = $4 - 12;
        } else {
            if ($4 < 12) {
                if ($4 > 0) {
                    $ampm = "AM"; $fixhr = $4 + 0;
                } else { # Hour is zero, so possibly midnight!
                    if (($5 > 0) || ($6 > 0)) {
                        $ampm = "AM"; $fixhr = 12;
                    } else {
                        $ampm = "Midnight"; $fixhr = 12;
                    }
                }
            } else { # Could be noon!
                if (($5 > 0) || ($6 > 0)) {
                    $ampm = "PM"; $fixhr = 12;
                } else {
                    $ampm = "Noon"; $fixhr = 12;
                }
            }
        }
        return ($2."/".$3."/".$YY." ".$fixhr.":".$5." ".$ampm) if ($format == 0);
        return ($2."/".$3."/".$YY." ".$4.":".$5) if ($format == 1);
        return ($fixhr.":".$5." ".$ampm) if ($format == 2);
        return ($4.":".$5) if ($format == 3);
    } else {
        croak "Bad input to time_display: $str";
    }
}
1;
# month_name(month) - Return the month name.
#
sub month_name {
    my $num = shift;
    $num--;
    @month = ("January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December");
    return $month[$num];
}
