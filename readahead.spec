Summary:	Read a preset list of files into memory
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
BuildRequires:	audit-libs-devel
BuildRequires:	e2fsprogs-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
readahead reads the contents of a list of files into memory, which
causes them to be read from cache when they are actually needed. Its
goal is to speed up the boot process.

%prep
%setup -q
cp -f -t ./lists/ %{SOURCE1}
cp -f -t ./lists/ %{SOURCE2}

%build
%configure \
	--sbindir=/sbin

%{__make}
%{__make} rpm-lists-rebuild RPM_LIB="%{_lib}" RPM_ARCH="%{_arch}" FILES="default.early default.later"

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING README lists/README.lists
%attr(755,root,root) /etc/cron.daily/readahead.cron
%attr(755,root,root) /etc/rc.d/init.d/readahead_later
%attr(755,root,root) /etc/rc.d/init.d/readahead_early
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/readahead.conf
%dir %{_sysconfdir}/readahead.d
%attr(644,root,root) %config %{_sysconfdir}/readahead.d/default.early
%attr(644,root,root) %config %{_sysconfdir}/readahead.d/default.later
%attr(755,root,root) %{_sbindir}/readahead
/sbin/readahead-collector

%preun
if [ "$1" = "0" ] ; then
 /sbin/chkconfig --del readahead_later
 /sbin/chkconfig --del readahead_early
fi

%post
/sbin/chkconfig --add readahead_later
/sbin/chkconfig --add readahead_early
