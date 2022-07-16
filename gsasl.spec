#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	kerberos5	# GSSAPI mechanism
%bcond_with	gss		# GNU GSS as GSSAPI implementation
%bcond_with	gssglue		# libgssglue GSSAPI wrapper
%bcond_without	heimdal		# Heimdal as GSSAPI implementation (default)
%bcond_with	krb5		# MIT Kerberos as GSSAPI implementation
%bcond_without	ntlm		# NTLM mechanism
%bcond_without	static_libs	# static library

%if %{with gss} || %{with gssglue} || %{with krb5}
%undefine	with_heimdal
%endif
%if %{without kerberos5}
%undefine	with_gss
%undefine	with_gssglue
%undefine	with_heimdal
%undefine	with_krb5
%endif
Summary:	GNU SASL - implementation of the Simple Authentication and Security Layer
Summary(pl.UTF-8):	GNU SASL - implementacja Simple Authentication and Security Layer
Name:		gsasl
Version:	2.0.1
Release:	1
License:	LGPL v2.1+ (library), GPL v3+ (gsasl tool)
Group:		Libraries
Source0:	https://ftp.gnu.org/gnu/gsasl/%{name}-%{version}.tar.gz
# Source0-md5:	8fdc487ff9121d0903ac7e3edcd35cd0
Patch0:		%{name}-info.patch
URL:		http://www.gnu.org/software/gsasl/
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.13
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-tools >= 0.19.8
BuildRequires:	gnutls-devel >= 3.4
%{?with_gss:BuildRequires:	gss-devel >= 1.0.0}
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.14}
%{?with_heimdal:BuildRequires:	heimdal-devel}
%{!?with_apidocs:BuildRequires:	help2man}
%{?with_krb5:BuildRequires:	krb5-devel}
BuildRequires:	libgcrypt-devel >= 1.3.0
%{?with_gssglue:BuildRequires:	libgssglue-devel}
BuildRequires:	libidn-devel >= 0.1.0
%{?with_ntlm:BuildRequires:	libntlm-devel >= 0.3.5}
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRequires:	texinfo
Requires(post,postun):	/sbin/ldconfig
Requires:	libgcrypt >= 1.3.0
%{?with_ntlm:Requires:	libntlm >= 0.3.5}
Obsoletes:	libgsasl < 0.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNU SASL is an implementation of the Simple Authentication and
Security Layer framework and a few common SASL mechanisms. SASL is
used by network servers (e.g., IMAP, SMTP) to request authentication
from clients, and in clients to authenticate against servers.

GNU SASL contains a library (`libgsasl'), a command line utility
(`gsasl') to access the library from the shell, and a manual. The
library includes support for the SASL framework (with authentication
functions and application data privacy and integrity functions) and at
least partial support for the CRAM-MD5, EXTERNAL, GSSAPI, ANONYMOUS,
PLAIN, SECURID, DIGEST-MD5, LOGIN, NTLM and KERBEROS_V5 mechanisms.

The library is portable because it does not do network communication
by itself, but rather leaves it up to the calling application. The
library is flexible with regards to the authorization infrastructure
used, as it utilizes callbacks into the application to decide whether
an user is authorized or not.

%description -l pl.UTF-8
GNU SASL to implementacja szkieletu Simple Authentication and Security
Layer (prostej warstwy uwierzytelniania i bezpieczeństwa) oraz kilku
popularnych mechanizmów SASL. SASL jest używane przez serwery sieciowe
(np. IMAP i SMTP) do żądania uwierzytelnienia od klientów oraz w
klientach do uwierzytelniania względem serwerów.

GNU SASL zawiera bibliotekę (libgsasl), narzędzie działające z linii
poleceń (gsasl) pozwalające na korzystanie z biblioteki z poziomu
powłoki oraz dokumentację. Biblioteka ma obsługę szkieletu SASL (z
funkcjami uwierzytelniającymi oraz zapewniającymi prywatność i
spójność danych aplikacji) oraz przynajmniej częściową obsługę
mechanizmów CRAM-MD5, EXTERNAL, GSSAPI, ANONYMOUS, PLAIN, SECURID,
DIGEST-MD5, LOGIN, NTLM oraz KERBEROS_V5.

Biblioteka jest przenośna, ponieważ sama nie korzysta z komunikacji
sieciowej, pozostawiając to wywołującej ją aplikacji. Biblioteka jest
elastyczna ze względu na używaną infrastrukturę uwierzytelniania,
ponieważ korzysta z callbacków w aplikacji przy decydowaniu, czy
użytkownik jest autoryzowany.

%package devel
Summary:	Header files for GNU SASL library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki GNU SASL
License:	LGPL v2.1+
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%if %{with gss}
Requires:	gss-devel >= 1.0.0
%else
%{?with_heimdal:Requires:	heimdal-devel}
%endif
Requires:	libgcrypt-devel >= 1.3.0
%{?with_gssglue:Requires:	libgssglue-devel}
Requires:	libidn-devel >= 0.1.0
%{?with_ntlm:Requires:	libntlm-devel >= 0.3.5}
Obsoletes:	libgsasl-devel < 0.1

%description devel
Header files for GNU SASL library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki GNU SASL.

%package static
Summary:	Static GNU SASL library
Summary(pl.UTF-8):	Statyczna biblioteka GNU SASL
License:	LGPL v2.1+
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	libgsasl-static < 0.1

%description static
Static GNU SASL library.

%description static -l pl.UTF-8
Statyczna biblioteka GNU SASL.

%package apidocs
Summary:	API documentation for GNU SASL library
Summary(pl.UTF-8):	Dokumentacja API biblioteki GNU SASL
Group:		Documentation
Conflicts:	gsasl-devel < 1.8.0-5
BuildArch:	noarch

%description apidocs
API documentation for GNU SASL library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki GNU SASL.

%prep
%setup -q
%patch0 -p1

%{__rm} po/stamp-po
# use system file (from gettext-tools)
%{__rm} m4/lib-link.m4

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I m4 -I lib/m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{?with_apidocs:--enable-gtk-doc} \
	%{!?with_ntlm:--disable-ntlm} \
	%{!?with_static_libs:--disable-static} \
	--with-gssapi-impl=%{?with_gss:gss}%{?with_gssglue:gssglue}%{?with_heimdal:heimdal}%{?with_krb5:mit}%{!?with_kerberos5:no} \
	--with-html-dir=%{_gtkdocdir} \
	--with-libgcrypt

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libgsasl.la

# libgsasl for lib, gsasl for app
%find_lang %{name} --all-name

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

%postun
/sbin/ldconfig
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS
%attr(755,root,root) %{_bindir}/gsasl
%attr(755,root,root) %{_libdir}/libgsasl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgsasl.so.18
%{_mandir}/man1/gsasl.1*
%{_infodir}/gsasl.info*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgsasl.so
%{_includedir}/gsasl*.h
%{_pkgconfigdir}/libgsasl.pc
%{_mandir}/man3/gsasl_*.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgsasl.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gsasl
%endif
