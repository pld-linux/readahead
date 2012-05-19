# TODO
# - maybe some scripts (still) usable here: http://bugs.gentoo.org/show_bug.cgi?id=64724
# - PLD-ize init.d scripts

Summary:	Read a preset list of files into memory
Summary(pl.UTF-8):	Odczyt predefiniowanej listy plików do pamięci
Name:		readahead
Version:	1.5.6
Release:	0.3
Epoch:		1
License:	GPL v2+
Group:		Base
# Source available only via git. Commands to get archive with latest released
# tag looks like:
# git clone git://git.fedorahosted.org/readahead
# cd readahead
# git archive --prefix=readahead-1.5.4/ v1.5.4 |bzip2 -9 >readahead-1.5.4.tar.bz2
Source0:	%{name}-%{version}.tar.bz2
# Source0-md5:	2c838de91b3501a378e72f3b7cf7bd11
Source1:	default.early
Source2:	default.later
Patch0:		%{name}-init.d.patch
URL:		https://fedorahosted.org/readahead/
BuildRequires:	audit-libs-devel >= 1.5
BuildRequires:	e2fsprogs-devel
BuildRequires:	libblkid-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
readahead reads the contents of a list of files into memory, which
causes them to be read from cache when they are actually needed. Its
goal is to speed up the boot process.

%description -l pl.UTF-8
readahead czyta zawartość plików z listy do pamięci. Powoduje to
czytanie ich z pamięci podręcznej (cache) gdy są faktycznie potrzebne.
Dzięki temu przyspieszany jest proces startowania systemu.

%prep
%setup -q
%patch0 -p1

%{__sed} -i "s,%{_prefix}%{_sbindir}/readahead,%{_sbindir}/readahead,g" scripts/readahead_*

%build
./autogen.sh
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/var/lib/readahead
install %{SOURCE1} $RPM_BUILD_ROOT/var/lib/readahead/
install %{SOURCE2} $RPM_BUILD_ROOT/var/lib/readahead/

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add readahead_later
/sbin/chkconfig --add readahead_early
%service readahead_early restart
%service readahead_later restart

%preun
if [ "$1" = "0" ]; then
	%service readahead_later stop
	%service readahead_early stop
	/sbin/chkconfig --del readahead_later
	/sbin/chkconfig --del readahead_early
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README lists/README.lists
%dir /etc/sysconfig/readahead
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/readahead.conf
%config(noreplace) %verify(not md5 mtime size) /etc/init/readahead.conf
%config(noreplace) %verify(not md5 mtime size) /etc/init/readahead-collector.conf
%config(noreplace) %verify(not md5 mtime size) /etc/init/readahead-disable-services.conf
%attr(755,root,root) /etc/cron.daily/readahead.cron
%attr(755,root,root) /etc/cron.monthly/readahead-monthly.cron
%attr(754,root,root) /etc/rc.d/init.d/readahead_later
%attr(754,root,root) /etc/rc.d/init.d/readahead_early
%attr(755,root,root) %{_sbindir}/readahead
%attr(755,root,root) %{_sbindir}/readahead-collector
%dir /var/lib/readahead
/var/lib/readahead/default.*
