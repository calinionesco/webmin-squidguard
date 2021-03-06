#!/usr/bin/perl
#
#    SquidGuard Configuration Webmin Module
#    Copyright (C) 2001 by Tim Niemueller <tim@niemueller.de>
#    http://www.niemueller.de/webmin/modules/squidguard/
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    Created  : 21.05.2001


require "./squidguard-lib.pl";

# ACL Check
if (! $access{'esource'}) {
  &terror('ssr_acl');
}

&error_setup($text{'ssr_error'});


if (defined($in{'delete'})) {
  &redirect("del_statement.cgi?sectype=source&secname=$in{'sourcegroup'}&index=$in{'index'}&back=sourcegroup");
} else {

  @config = &parse_config();

  my $sec=&find_section( 'sectype' => "source",
                         'secname' => $in{'sourcegroup'},
                         'config'  => \@config );
  &terror('esg_err_notfound', $in{'sourcegroup'}) if (! defined($sec));
  my $st=$sec->{'members'}->[$in{'index'}] if (! $in{'new'});


  # Check input
  &terror('ssr_inv_begin') if ($in{'begin'} !~ /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/);
  &terror('ssr_inv_end') if ($in{'end'} !~ /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/);
  my $start = &numberize($in{'begin'});
  my $end = &numberize($in{'end'});
  &terror('ssr_inv_range') if ($end <= $start);

  # Create a new line
  my $newline = "ip\t\t$in{'begin'}-$in{'end'}";

  # Save the new line replacing the old one
  my $conf = &read_file_lines($config{'conf'});
  if ($in{'new'}) {
    # Adding a new statement
    my @newlines=($conf->[$sec->{'line'}],
                  "\t$newline" );
    splice(@$conf, $sec->{'line'}, 1, @newlines);
  } else {
    # Modifying a statement
    $conf->[$st->{'line'}]="\t$newline";
  }
  &flush_file_lines();
  &sgchown($config{'conf'});

  if ($in{'new'}) {
    &redirect("edit_sourcegroup.cgi?sourcegroup=$in{'sourcegroup'}");
  } else {
    &redirect("edit_sourcerange.cgi?sourcegroup=$in{'sourcegroup'}&index=$in{'index'}");
  }

}


# Helper functions

sub numberize {
 (my $a, my $b, my $c, my $d) = split(/\./, $_[0]);
 return(($a << 24) | ($b << 16) | ($c << 8) |  $d);
}

sub denumberize {
 my $tmpstr=join('.', ($_[0] & 0xff000000) >> 24,
                     ($_[0] & 0x00ff0000) >> 16,
                     ($_[0] & 0x0000ff00) >> 8,
                     ($_[0] & 0x000000ff) );
$tmpstr;
}


### END of save_sourcerange.cgi ###.
