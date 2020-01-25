#!/usr/bin/perl
use File::Basename;
use CGI qw(:param);
use lib '.';
use aswe;

my $template = param('template');
my $debug = param('debug');

print "Content-type: text/html\n\n";

printparams if defined $debug;

$template = readparam('.template') if $template eq '';
fcat("$ENV{'DOCUMENT_ROOT'}$template") if $template ne '';
