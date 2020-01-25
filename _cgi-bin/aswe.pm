package aswe;
require Exporter;
@ISA=qw(Exporter);
@EXPORT=qw(
	    freadstr
	    freadfile
	    fcat
	    geturi
	    readparam
	    printparams
	);

use File::Basename;
use CGI qw(:param);

use constant SubHost=>1;

#читает строку из файла (вместо cat-a в строку)
sub freadstr
{
    return unless -f @_[0];
    open(FIL,@_[0]);
    my $a = <FIL>;
    chomp $a;
    close(FIL);
    return $a;
}

#читает файл в переменную (вместо cat-а в переменную)
sub freadfile
{
    return unless -f @_[0];
    open(FIL,@_[0]);
    my $i = join('',<FIL>);
    close(FIL);
    return $i;
}

#печатает файл (вместо cat-a)
sub fcat
{
    return unless -f @_[0];
    open(FIL,@_[0]);
    while(<FIL>)
    {
	print;
    }
    close(FIL);
}

#строит путь к каталогу по DOCUMENT_URI
sub geturi
{
    return defined $ENV{'DOCUMENT_URI'}?(-T $ENV{'DOCUMENT_ROOT'}.$ENV{'DOCUMENT_URI'}?dirname($ENV{'DOCUMENT_URI'})."/":$ENV{'DOCUMENT_URI'}):'.';
}

#читает параметр из файла по имени
sub readparam
{
    my ($file,$template) = @_;
    my $uri = geturi;
    my $path = $ENV{'DOCUMENT_ROOT'} . $uri;

    $template = freadstr("$path/$file") if $template eq '';			#если шаблон не передали пытаемся взять из текущего каталога
    if( $template eq '' and SubHost == 1 )					#если шаблон все еще пуст - берем из первого каталога (на случай если это ссылка на сайт на сайте)
    {
#	$path =~ s/^(.+)\/.+$/$1/;			#взять из предыдущего каталога - наверное неправильно
	$uri =~ s/^(\/.+)\/.+/$1/;			#возьмем из первого
	$template = freadstr("$ENV{'DOCUMENT_ROOT'}$uri/$file");
    }
    $template = freadstr("$ENV{'DOCUMENT_ROOT'}/$file") if $template eq '';	#если шаблон все еще пуст - берем из корня

    return $template;
}

#для дебага - печатает параметры
sub printparams
{
#print "<table>\n";
#for my $i (keys %ENV)
#{
#    print "<tr><td>$i<td>$ENV{$i}\n";
#}
#print "</table>\n";
    print "<pre>\n";
    print "DOCUMENT_ROOT=$ENV{'DOCUMENT_ROOT'}\nDOCUMENT_URI=$ENV{'DOCUMENT_URI'}\n";
    for my $i (param())
    {
	print "$i=[",param($i),"]\n";
    }
}
1;
