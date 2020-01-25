#!/usr/bin/perl
use File::Basename;
use CGI qw(:param);
use lib '.';
use aswe;

#print "<table>\n";
#for my $i (keys %ENV)
#{
#    print "<tr><td>$i<td>$ENV{$i}\n";
#}
#print "</table>\n";

my $pref = param('pref');
my $post = param('post');
my $template = param('template');
my $expired = param('expired');
my $type = param('type');

$type = 'bnr' if $type eq '';

print "\n\n";
#print "$path\n";
#print "<pre>\n$template</pre>\n";
printlevel(-T $ENV{'DOCUMENT_ROOT'}.$ENV{'DOCUMENT_URI'}?dirname($ENV{'DOCUMENT_URI'})."/":$ENV{'DOCUMENT_URI'});

sub printlevel
{
    my ($uri) = @_;
    my $path = $ENV{'DOCUMENT_ROOT'} . $uri;
    my $flag = 0;

    opendir TDIR, $path or die "No such directory\n";
    my %tdir = map {substr($_,6,2).substr($_,0,6),"$path$_"} grep /^\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])(\d{2})_.+\.($type)$/, readdir TDIR;
    closedir TDIR;
#print "<pre>\n";
    for my $i (sort keys %tdir)
    {
	if($expired == 1)
	{
	    $i =~ /^\d{2}(\d{2})(\d{2})(\d{2})/;
	    my ($y,$m,$d) = ($1,$2,$3);
	    my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
	    next if $y < $year - 100;
	    next if $y == $year - 100 and $m < $mon + 1;
	    next if $y == $year - 100 and $m == $mon + 1 and $d < $mday;
	}
	my %defs = map {eqsplit($_)} `cat $tdir{$i}`;
	print $pref if $pref ne '';
	if($template ne '')
	{
	    my $s = $template;
	    map {$s =~ s/$_/$defs{$_}/g} keys %defs;
	    print $s;
	}
#        print `cat $i`;
#print "$i",$tdir{$i},"\n";
#print join(',',keys(%defs)),"\n";
#print join(',',values(%defs)),"\n";
	print $post if $post ne '';
    }
}

sub eqsplit
{
#print "<br>[$_]<br>\n";
    /^(.+)=([^\r\n]*)/;
    return ($1,$2);
}
