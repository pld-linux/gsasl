#
# Conditional build:
%bcond_with	apidocs		# disable gtk-doc
%bcond_with	gss		# use gss instead of Heimdal as GSSAPI implementation
%bcond_with	kerberos5	# with KERBEROS_V5 mechanism (based on shishi, currently broken)
%bcond_without	heimdal		# do not use Heimdal either
%bcond_without	ntlm		# without NTLM mechanism
%bcond_without	static_libs	# don't build static libraries

Summary:	GNU SASL - implementation of the Simple Authentication and Security Layer
Summary(pl.UTF-8):	GNU SASL - implementacja Simple Authentication and Security Layer
Name:		gsasl
Version:	1.8.0
Release:	7
License:	LGPL v2.1+ (library), GPL v3+ (gsasl tool)
Group:		Libraries
Source0:	http://ftp.gnu.org/gnu/gsasl/%{name}-%{version}.tar.gz
# Source0-md5:	982fe54a20016aa46a871c084c990c36
Patch0:		%{name}-info.patch
Patch1:		%{name}-heimdal-check.patch
Patch2:		%{name}-link.patch
URL:		http://www.gnu.org/software/gsasl/
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake >= 1:1.10
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-tools >= 0.18.1
BuildRequires:	gnutls-devel >= 1.2.0
%{?with_gss:BuildRequires:	gss-devel >= 1.0.0}
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.1}
%{!?with_apidocs:BuildRequires:	help2man}
# used by examples/saml20 (noinst only)
#BuildRequires:	lasso-devel >= 2.2.1
BuildRequires:	libgcrypt-devel >= 1.3.0
BuildRequires:	libidn-devel >= 0.1.0
%{?with_ntlm:BuildRequires:	libntlm-devel >= 0.3.5}
BuildRequires:	libtool >= 2:1.5
BuildRequires:	pkgconfig
%if %{without gss}
# alternatively, gss or krb5 can be used for GSSAPI
%{?with_heimdal:BuildRequires:	heimdal-devel}
%endif
%{?with_kerberos5:BuildRequires:	shishi-devel}
BuildRequires:	texinfo
Requires(post,postun):	/sbin/ldconfig
Requires:	libgcrypt >= 1.3.0
%{?with_ntlm:Requires:	libntlm >= 0.3.5}
Obsoletes:	libgsasl
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
Requires:	libidn-devel >= 0.1.0
%{?with_ntlm:Requires:	libntlm-devel >= 0.3.5}
%{?with_kerberos5:Requires:	shishi-devel}
Obsoletes:	libgsasl-devel

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
Obsoletes:	libgsasl-static

%description static
Static GNU SASL library.

%description static -l pl.UTF-8
Statyczna biblioteka GNU SASL.

%package apidocs
Summary:	API documentation for GNU SASL library
Summary(pl.UTF-8):	Dokumentacja API biblioteki GNU SASL
Group:		Documentation
Conflicts:	gsasl-devel < 1.8.0-5
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for GNU SASL library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki GNU SASL.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%{__rm} po/stamp-po
# use system file (from gettext-tools)
%{__rm} lib/m4/lib-link.m4

# remove it when "linking libtool libraries using a non-POSIX archiver ..." warning is gone
# (after gsasl or libtool change)
%{__sed} -i -e '/AM_INIT_AUTOMAKE/s/-Werror//' configure.ac lib/configure.ac

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I m4 -I gl/m4
%{__autoconf}
%{__autoheader}
%{__automake}
cd lib
%{__libtoolize}
%{__aclocal} -I m4 -I gl/m4
%{__autoconf}
%{__autoheader}
%{__automake}
cd -
%configure \
	--disable-silent-rules \
	%{?with_apidocs:--enable-gtk-doc} \
	%{!?with_ntlm:--disable-ntlm} \
	%{!?with_static_libs:--disable-static} \
	%{?with_kerberos5:--enable-kerberos_v5} \
%if %{with gss}
	--with-gssapi-impl=gss
%else
	%{?with_heimdal:--with-gssapi-impl=heimdal} \
	%{!?with_heimdal:--with-gssapi-impl=no} \
%endif
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
%doc AUTHORS ChangeLog NEWS README* THANKS
%attr(755,root,root) %{_bindir}/gsasl
%attr(755,root,root) %{_libdir}/libgsasl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgsasl.so.7
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
