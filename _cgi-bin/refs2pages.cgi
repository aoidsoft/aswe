#!/usr/bin/perl
use File::Basename;
use CGI qw(:param);
use lib '.';
use aswe;

my $template = param('template');
my $pref = param('pref');
my $post = param('post');
my $tree = param('tree');
my $from = param('from');

#параметры по умолчанию
$post = "</$1>" if $pref =~ /<(\w+)>/ and not defined param('post');		#если pref определили как html-тэг, а закрыть забыли (не задан post)

#main
if($from eq '')
{
    $from = $ENV{'DOCUMENT_URI'};
}
elsif($from eq '//')
{
    $from = $ENV{'DOCUMENT_URI'};
    $from = $1 if $from =~ /^(\/[\w\s\%]+\/)/;
}

$tree = 1 if $tree eq '';

print "\n\n";
#print "$path\n";
#print "<pre>\n$template</pre>\n";

#print "<table>\n";
#for my $i (keys %ENV)
#{
#    print "<tr><td>$i<td>$ENV{$i}\n";
#}
#print "</table>\n";

#print "<pre>\n";
#print "DOCUMENT_ROOT=$ENV{'DOCUMENT_ROOT'}\n";
#print "DOCUMENT_URI=$ENV{'DOCUMENT_URI'}\n";
#print "</pre>\n";

printlevel(-T $ENV{'DOCUMENT_ROOT'}.$from?(dirname($from) ne '/'?dirname($from).'/':'/'):$from);

sub printlevel
{
#print "<pre>\n\n";
    my ($uri) = @_;
    my $path = $ENV{'DOCUMENT_ROOT'} . $uri;
    my $flag = 0;
#print "$path\n";
    opendir TDIR, $path or die "No such directory\n";
    my @tdir = grep /^\d{2}_.+/, readdir TDIR;
    closedir TDIR;
#print "tdir=",join(',',@tdir),"\n";
    for my $i (sort @tdir)
    {
#print "i=$i\n";
        my $r = $template;
        my $page;
	my $dir = $i;
        my $puri = $uri . $i;
        $i =~ /^\d{2}_(.+)$/;
        my $ppath = "$path$i/$1";
	for my $j (qw/shtml html htm/)
	{
#print "ppath=$ppath\n";
    	    if(-T "$ppath.$j")
    	    {
    		$page = "$ppath.$j";
    		$puri .= "/$1.$j";
		break;
    	    }
	}
	my $tmp = freadstr("$path$i/.title");
	if( $tmp ne '' )
	{
	    $i = $tmp;
	} else {
	    if($page ne '')
	    {
		$tmp = freadfile($page);
		$i = $1 if $tmp =~ /<title>(.+)<\/title>/i;
	    }
        }
        $r =~ s/\@{2}/$puri/g;
        $r =~ s/\${2}/$i/g;

	print $pref if $pref ne '' and !$flag;
	$flag++;
	
        print "$r\n";
#print "$uri$dir/\n";
	printlevel("$uri$dir/") if $tree == 1;
    }
    print $post if $flag;
}
