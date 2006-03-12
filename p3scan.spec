Summary:	An application level gateway for the POP3 protocol
Summary(pl):	Brama warstwy aplikacji dla protoko³u POP3
Name:		p3scan
Version:	2.3.2
Release:	1
License:	GPL
Group:		Applications/Networking
Source0:	http://dl.sourceforge.net/p3scan/%{name}-%{version}.tar.gz
# Source0-md5:	9f8decc7d4701228788e3c8717096ca0
Source1:	%{name}.init
Patch0:		%{name}-config.patch
URL:		http://p3scan.sourceforge.net/
BuildRequires:	pcre-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	pcre
Requires:	rc-scripts
# FIXME: which package in PLD provides 'netfilter' ?
#Requires:	netfilter
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_sysconfdir	/etc/%{name}

%description
p3scan provides transparent antivirus scanner gateway for the POP3
protocol.

%description -l pl
p3scan dostarcza przezroczystej bramki antywirusowej dla protoko³u
POP3.

%prep
%setup -q
%patch0 -p1

%build
rm -fr ripmime/ripmime.a
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir},/etc/rc.d/init.d,%{_mandir}/man8}
install -d $RPM_BUILD_ROOT{/var/spool/%{name}/{notify,children},/var/run/%{name}}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{name}.conf $RPM_BUILD_ROOT%{_sysconfdir}
install %{name}-*.mail $RPM_BUILD_ROOT%{_sysconfdir}
install %{name} $RPM_BUILD_ROOT%{_sbindir}
gzip -dc %{name}.8.gz > $RPM_BUILD_ROOT%{_mandir}/man8/%{name}.8
gzip -dc %{name}_readme.8.gz > $RPM_BUILD_ROOT%{_mandir}/man8/%{name}_readme.8

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%triggerin -- clamav
chown -R clamav /var/spool/%{name}
chown -R clamav /var/run/%{name}

%triggerun -- clamav
if [ $2 = 0 ]; then
	chown -R root /var/spool/%{name}
	chown -R root /var/run/%{name}
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG CONTRIBUTERS README TODO.list
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) %{_sbindir}/*
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}-*.mail
%attr(770,root,mail) %dir /var/spool/%{name}
%attr(770,root,mail) %dir /var/spool/%{name}/notify
%attr(770,root,mail) %dir /var/spool/%{name}/children
%attr(770,root,mail) %dir /var/run/%{name}
%{_mandir}/man8/*
