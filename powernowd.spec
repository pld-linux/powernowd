Summary:	CPU frequency scaling daemon
Summary(pl):	Demon skalowania czêstotliwo¶ci procesora
Name:		powernowd
Version:	0.96
Release:	0.1
License:	GPL
Group:		Daemons
Source0:	http://www.deater.net/john/%{name}-%{version}.tar.gz
# Source0-md5:	9c7131bce36bbb3e8b688478e8dc34c7
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://www.deater.net/john/powernowd.html
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Powernowd reduces CPU's freuency when it is idle.

%description -l pl
Powernowd s³u¿y do zmniejszania czêstotliwo¶ci procesora podczas jego
bezczynno¶ci.

%prep
%setup -q

%build
%{__make}

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
if [ -f /var/lock/subsys/powernowd ]; then
	/etc/rc.d/init.d/powernowd restart >&2
else
	echo "Run \"/etc/rc.d/init.d/powernowd start\" to start powernowd daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/powernowd ]; then
		/etc/rc.d/init.d/powernowd stop>&2
	fi
	/sbin/chkconfig --del powernowd
fi

%files
%defattr(644,root,root,755)
%doc README
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/%{name}

# initscript and its config
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
