Name:           tinyxml
Version:        2.6.2
Release:        0%{?dist}
Summary:        A simple, small, C++ XML parser
Group:          System Environment/Libraries
License:        zlib
URL:            http://www.grinninglizard.com/tinyxml/
Source0:        %{name}-%{version}.tar.gz
Source1001:     %{name}.manifest

%description
TinyXML is a simple, small, C++ XML parser that can be easily integrating
into other programs. Have you ever found yourself writing a text file parser
every time you needed to save human readable data or serialize objects?
TinyXML solves the text I/O file once and for all.
(Or, as a friend said, ends the Just Another Text File Parser problem.)


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
cp %{SOURCE1001} .
#touch -r tinyxml.h.stl tinyxml.h

%build
# Not really designed to be build as lib, DYI
for i in tinyxml.cpp tinystr.cpp tinyxmlerror.cpp tinyxmlparser.cpp; do
  g++ -std=c++11 -fPIC -o $i.o -c $i
done
g++ -shared -std=c++11 -o lib%{name}.so.0.%{version} \
   -Wl,-soname,lib%{name}.so.0 *.cpp.o


%install
# Not really designed to be build as lib, DYI
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}
install -m 755 lib%{name}.so.0.%{version} %{buildroot}%{_libdir}
ln -s lib%{name}.so.0.%{version} %{buildroot}%{_libdir}/lib%{name}.so.0
ln -s lib%{name}.so.0.%{version} %{buildroot}%{_libdir}/lib%{name}.so
install -p -m 644 %{name}.h %{buildroot}%{_includedir}
install -p -m 644 tinystr.h %{buildroot}%{_includedir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%doc changes.txt readme.txt
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc docs/*
%{_includedir}/*
%{_libdir}/*.so

%changelog
* Fri Dec 14 2007 Hans de Goede <j w r degoede hhs nl> 2.5.3-2
- Various improvements from review (bz 407571)

* Fri Nov 30 2007 Hans de Goede <j w r degoede hhs nl> 2.5.3-1
- Initial Fedora Package
