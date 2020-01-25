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
    my @tdir = map "$path$_", grep /^\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{2}_.+\.(htm|txt)$/, readdir TDIR;
    closedir TDIR;

    for my $i (sort @tdir)
    {
	print $pref if $pref ne '';
	fcat($i);
	print $post if $post ne '';
    }
}
