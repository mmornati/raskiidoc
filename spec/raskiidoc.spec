Summary: RaskiiDoc Builder
Name: raskiidoc
Version: 1.2
Release: 1
License: GPLv3
Group: Applications/System
URL: https://github.com/llicour/raskiidoc
Source: %{name}-%{version}.tar.gz

%description
%{summary}.

Summary: RaskiiDoc Builder
Requires: rubygem-rake, rake, python-argparse, asciidoc >= 8.6.0, source-highlight, asciidoc-latex, texlive-upquote
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch

%package template-think
Summary: Template for Think Company
Group: Applications/System
Requires: raskiidoc,texlive-inconsolata

%description template-think
%{summary}

%prep
%setup -n %{name}

%build

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__mkdir} -p $RPM_BUILD_ROOT/%_sbindir
%{__mkdir} -p $RPM_BUILD_ROOT/usr/share/raskiidoc
%{__mkdir} -p $RPM_BUILD_ROOT/etc/raskiidoc

%{__cp} -R ./Rakefile $RPM_BUILD_ROOT/usr/share/%{name}
%{__cp} -R ./raskiidoc/* $RPM_BUILD_ROOT/usr/share/%{name}
#%{__cp} ./scripts/* $RPM_BUILD_ROOT/usr/sbin
install -m 0755 ./scripts/raskiidoc $RPM_BUILD_ROOT/%_sbindir/raskiidoc
%{__cp} ./conf/* $RPM_BUILD_ROOT/etc/raskiidoc

#create version file

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%exclude /usr/share/raskiidoc/raskiidoc.d/think-*
%exclude /usr/share/raskiidoc/dblatex/think.sty.tpl
%defattr(-,root,root,-) 
%config(noreplace) /etc/raskiidoc/*
%config /usr/share/raskiidoc/raskiidoc.yaml
/usr/sbin/raskiidoc
/usr/share/%{name}/*

%files template-think
%defattr(-,root,root,-)
/usr/share/raskiidoc/raskiidoc.d/think-*
/usr/share/raskiidoc/dblatex/think.sty.tpl

%doc
#%attr(0755,root,root) %dir /usr/share/%{name}
#%attr(0755,root,root) /usr/sbin/raskiidoc
#%attr(0644,root,root) %dir /etc/raskiidoc

%pre

%post

%preun

%postun

%changelog
