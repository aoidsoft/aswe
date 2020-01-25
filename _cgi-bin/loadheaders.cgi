#!/usr/bin/perl
use File::Basename;
use CGI qw(:param);
use lib '.';
use aswe;

#считываемые параметры скрипта
my $filemask = param('filemask');	#regexp-маска имени файла, по умолчанию вида: YYMMDD_*.(htm|txt)
my $filepref = param('filepref');	#префикс ($filepref) имени файла вида: $filepref$filemask
my $template = param('template');
my $pref = param('pref');
my $post = param('post');
my $lines = param('lines');
my $count = param('count');
my $next = param('next');
my $preed = param('preed');
my $any = param('any');
my $back = param('back');		#порядок сортировки, 0 обычный (по умолчанию), 1 обратный
my $current = param('current');
my $ponly = param('ponly');
my $endcheck = param('endcheck');
my $debug = param('debug');
my $page = 0;

#параметры по умолчанию для пустых
$filemask = '^\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{2}_.+\.(htm|txt)$' if $filemask eq '';
#printf "filemask=$filemask\n";

$filemask =~ s/^(\^|)(.+)/$1$filepref$2/ if $filepref ne '';
#printf "filepref=$filepref\n";
#printf "filemask=$filemask\n";

$post = "</$1>" if $pref =~ /<(\w+)>/ and not defined param('post');		#если pref определили как html-тэг, а закрыть забыли (не задан post)
#exit;

#main
if(defined $ENV{'QUERY_STRING_UNESCAPED'} and $ENV{'QUERY_STRING_UNESCAPED'} =~ /page=(\d+)/)
{
    $page = $1 - 1 if $1 > 0;
}

print "\n\n";
#print "$path\n";
#print "<pre>\n$template</pre>\n";
#print "<table>\n";
#for my $i (keys %ENV)
#{
#    print "<tr><td>$i<td>$ENV{$i}\n";
#}
#print "</table>\n";
if($debug)
{
#print "<table>\n";
#for my $i (keys %ENV)
#{
#    print "<tr><td>$i<td>$ENV{$i}\n";
#}
#print "</table>\n";
    print "<pre>\n";
    print "DOCUMENT_ROOT=$ENV{'DOCUMENT_ROOT'}\nDOCUMENT_ROOT=$ENV{'DOCUMENT_URI'}\n";
    for my $i (param())
    {
	print "$i=[",param($i),"]\n";
    }
}

printlevel(-T $ENV{'DOCUMENT_ROOT'}.$ENV{'DOCUMENT_URI'}?dirname($ENV{'DOCUMENT_URI'})."/":$ENV{'DOCUMENT_URI'});

sub printlevel
{
    my ($uri) = @_;
    my $path = $ENV{'DOCUMENT_ROOT'} . $uri;
    my $flag = 0;
#print $ENV{'DOCUMENT_ROOT'} , $uri,"\n",$path;
    opendir TDIR, $path or die "No such directory\n";
#перебираем файлы с именем вида: YYMMDD_*.(htm|txt)
#    my @tdir = map "$path$_", grep /^\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{2}_.+\.(htm|txt)$/, readdir TDIR;
    my @tdir = map "$path$_", grep /$filemask/, readdir TDIR;
    closedir TDIR;
#print "\n",join("\n",@tdir),"\n";
#print "<br>$filemask<br>\n";

    my $beg = 0;
    my $end = scalar(@tdir);
    if($count > 0)
    {
	$beg = $page - ($page % $count);
	$end = $beg + $count;
    }
    my $curitem = 0;
    @tdir = sort @tdir;
    @tdir = reverse @tdir if $back == 1;
if($debug)
{
print "all=",scalar(@tdir),"\n";
print "count=$count\n";
print "beg=$beg\n";
print "end=$end\n";
print "page=$page\n";
print "curitem=$curitem\n";
}
    for(;$curitem < scalar(@tdir);$curitem++)
    {
	my $i = $tdir[$curitem];
print "$i\n" if $debug;
	if($count > 0)
	{
	    next if $curitem < $beg;
	    last if $curitem >= $end;
	}
	print $pref if $pref ne '';
	my $pfx;
	if($ponly != 1)
	{
	if($template ne '')
	{
	    my $r = $template;
	    my $puri = $i;
	    $puri =~ s/^$ENV{'DOCUMENT_ROOT'}//;
    	    $r =~ s/\@{2}/$puri/g;
    	    $r =~ /^(.+)\${2}(.+)$/;
	    print $1;
	    $pfx = $2;
	}
	unless($lines)
	{
	    fcat($i);
	}
	else
	{
	    open IN,$i or print $!;
	    for(my $j=0;$j++ < $lines and $_=<IN>;)
	    {
		print $_;
	    }
	    print '...' if $endcheck and <IN>;
	    close IN;
	}
	}
	print $pfx if $template ne '';
	print $post if $post ne '';
    }
    if($count > 0 and scalar(@tdir) > 1)
    {
	if($preed ne '' and $beg > 0)
	{
	    printpagelink($beg - 1,$preed);
	}
	if($any ne '' and scalar(@tdir) > 0)
	{
	    my $nend = $end < scalar(@tdir)?$end:scalar(@tdir);
	    for(my $j=$beg; $j < $nend; $j++)
	    {
		if($page != $j)
		{
		    printpagelink($j,$any);
		}
		else
		{
		    printpagelink($j,$current ne ''?$current:$j+1 . ' ');
		}
	    }
	}
	if($next ne '' and $end < scalar(@tdir))
	{
	    printpagelink($end,$next);
	}
    }
}

sub printpagelink
{
    my ($cpage,$next) = @_;
    $cpage++;
print "$cpage\n" if $debug;
    my $req = $ENV{'QUERY_STRING_UNESCAPED'};
    if($req eq '')
    {
	$req = "page=$cpage";
    }
    else
    {
	$req .= "&page=$cpage" unless $req =~ s/page=\d+/page=$cpage/;
    }
    $next =~ s/\${2}/$cpage/g;
    $next =~ s/\@{2}/$ENV{DOCUMENT_URI}?$req/g;
    print $next;
}
