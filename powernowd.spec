Summary:	CPU frequency scaling daemon
Summary(pl):	Demon skalowania czêstotliwo¶ci procesora
Name:		powernowd
Version:	0.97
Release:	1
License:	GPL
Group:		Daemons
Source0:	http://www.deater.net/john/%{name}-%{version}.tar.gz
# Source0-md5:	cc6f567e30c3797c17593fdc707f8a67
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://www.deater.net/john/powernowd.html
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Powernowd reduces CPU's freuency when it is idle.

%description -l pl
Powernowd s³u¿y do zmniejszania czêstotliwo¶ci procesora podczas jego
bezczynno¶ci.

%prep
%setup -q

%build
%{__cc} %{rpmcflags} %{rpmldflags} -o powernowd powernowd.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,%{_sbindir},%{_sysconfdir}/sysconfig}

install %{name} $RPM_BUILD_ROOT%{_sbindir}/%{name}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add powernowd
%service powernowd restart "powernowd daemon"

%preun
if [ "$1" = "0" ]; then
	%service powernowd stop
	/sbin/chkconfig --del powernowd
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
