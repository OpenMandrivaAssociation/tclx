%define major_ver	%(echo %{version}|cut -d. -f1,2)
%define libname		%mklibname %{name} %{version}
%define develname	%mklibname %name -d

%{!?tcl_version: %define tcl_version %(echo 'puts $tcl_version' | tclsh || echo 'Unknown version')}
%{!?tcl_sitearch: %define tcl_sitearch %{_libdir}/tcl%{tcl_version}}

Name:		tclx
Epoch:		0
Version:	8.4.1
Release:	%mkrel 12
Summary:	Tcl/Tk extensions for POSIX systems
License:	BSD
Group:		System/Libraries
URL:		http://tclx.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/tclx/tclx%{version}.tar.bz2
Patch1:		tclx-8.4-varinit.patch
Patch3:		tclx-8.4-man.patch
BuildRequires:	pkgconfig(tcl)
BuildRequires:	pkgconfig(tk)
BuildRequires:	groff


%description
TclX is a set of extensions which make it easier to use the Tcl
scripting language for common UNIX/Linux programming tasks.  TclX
enhances Tcl support for files, network access, debugging, math, lists,
and message catalogs.  TclX can be used with both Tcl and Tcl/Tk
applications.

Install TclX if you are developing applications with Tcl/Tk.  You'll
also need to install the tcl and tk packages.

%package -n	%{libname}
Summary:	Shared libraries for %{name}
Group:		System/Libraries
Requires:	tcl(abi) = %{tcl_version}
Requires:	tk
Provides:	%{name} = %{epoch}:%{version}-%{release}
Provides:	lib%{name} = %{epoch}:%{version}-%{release}


%description -n %{libname}
TclX is a set of extensions which make it easier to use the Tcl
scripting language for common UNIX/Linux programming tasks.  TclX
enhances Tcl support for files, network access, debugging, math, lists,
and message catalogs.  TclX can be used with both Tcl and Tcl/Tk
applications.

Install TclX if you are developing applications with Tcl/Tk.  You'll
also need to install the tcl and tk packages.

%package -n	%{develname}
Summary:	Development files for %{name}
Group:		Development/Other
Requires:	%{libname} = %{epoch}:%{version}
Provides:	%{name}-devel = %{epoch}:%{version}-%{release}
Provides:	lib%{name}-devel = %{epoch}:%{version}-%{release}

%description -n	%{develname}
This package contains development files for %{name}.

%prep
%setup -q -n tclx%{major_ver}
%autopatch -p1

%build
%configure2_5x \
	--enable-tk=YES \
	--with-tclconfig=%{_libdir} \
	--with-tkconfig=%{_libdir} \
	--with-tclinclude=%{_includedir} \
	--with-tkinclude=%{_includedir} \
	--libdir=%{tcl_sitearch} \
	--enable-gcc \
	--disable-threads \
	--enable-shared \
	--enable-64bit

# parallell build is borked!
%__make

%install
%make_install

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/
echo '%{_libdir}/tcl%{tcl_version}/%{name}%{major_ver}' > $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/%{name}%{major_ver}-%{_arch}.conf

%files -n %{libname}
%doc ChangeLog README
%{_sysconfdir}/ld.so.conf.d/%{name}%{major_ver}-%{_arch}.conf
%{tcl_sitearch}/tclx%{major_ver}

%files -n %{develname}
%{_includedir}/*.h
%{_mandir}/man3/*
%{_mandir}/mann/*
