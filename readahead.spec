# TODO
# - maybe some scripts (still) usable here: http://bugs.gentoo.org/show_bug.cgi?id=64724
Summary:	Read a preset list of files into memory
Summary(pl.UTF-8):	Odczyt predefiniowanej listy plików do pamięci 
Name:		readahead
Version:	1.4.1
Release:	0.1
Epoch:		1
License:	GPL
Group:		Base
Source0:	http://people.redhat.com/kzak/readahead/%{name}-%{version}.tar.bz2
# Source0-md5:	61436ab8695807f5e24908f080e5a1ae
Source1:	default.early
Source2:	default.later
URL:		https://hosted.fedoraproject.org/projects/readahead
BuildRequires:	audit-libs-devel >= 1.5
BuildRequires:	e2fsprogs-devel
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
cp -a %{SOURCE1} lists
cp -a %{SOURCE2} lists

%build
%configure

%{__make}
%{__make} rpm-lists-rebuild \
	RPM_LIB="%{_lib}" \
	RPM_ARCH="%{_arch}" \
	FILES="default.early default.later"

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add readahead_later
/sbin/chkconfig --add readahead_early

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del readahead_later
	/sbin/chkconfig --del readahead_early
fi

%files
%defattr(644,root,root,755)
%doc COPYING README lists/README.lists
%dir %{_sysconfdir}/readahead.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/readahead.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/readahead.d/default.early
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/readahead.d/default.later

%attr(755,root,root) /etc/cron.daily/readahead.cron
%attr(754,root,root) /etc/rc.d/init.d/readahead_later
%attr(754,root,root) /etc/rc.d/init.d/readahead_early
%attr(755,root,root) /usr/sbin/readahead
%attr(755,root,root) /sbin/readahead-collector
