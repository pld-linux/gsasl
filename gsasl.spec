#
# Conditional build:
%bcond_without	gss		# without GSSAPI mechanism
%bcond_without	krbv5		# without KERBEROS_V5 mechanism
%bcond_without	ntlm		# without NTLM mechanism
%bcond_without	static_libs	# don't build static libraries
#
Summary:	GNU SASL - implementation of the Simple Authentication and Security Layer
Summary(pl):	GNU SASL - implementacja Simple Authentication and Security Layer
Name:		gsasl
Version:	0.2.15
Release:	1
License:	GPL
Group:		Libraries
Source0:	http://josefsson.org/gsasl/releases/%{name}-%{version}.tar.gz
# Source0-md5:	906954c002098370c161ac2c97c4c33e
Patch0:		%{name}-info.patch
URL:		http://www.gnu.org/software/gsasl/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9
BuildRequires:	gettext-devel >= 0.14.1
BuildRequires:	gnutls-devel >= 1.2.0
%{?with_gss:BuildRequires:	gss-devel >= 0.0.0}
BuildRequires:	gtk-doc >= 1.1
BuildRequires:	libgcrypt-devel >= 1.1.42
BuildRequires:	libidn-devel >= 0.1.0
%{?with_ntlm:BuildRequires:	libntlm-devel >= 0.3.5}
BuildRequires:	libtool >= 2:1.5
BuildRequires:	pkgconfig
# alternatively, krb5 or heimdal could be used for GSSAPI and KERBEROS_V5
%{?with_krbv5:BuildRequires:	shishi-devel >= 0.0.0}
BuildRequires:	texinfo
Requires(post,postun):	/sbin/ldconfig
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

%description -l pl
GNU SASL to implementacja szkieletu Simple Authentication and Security
Layer (prostej warstwy uwierzytelniania i bezpieczeñstwa) oraz kilku
popularnych mechanizmów SASL. SASL jest u¿ywane przez serwery sieciowe
(np. IMAP i SMTP) do ¿±dania uwierzytelnienia od klientów oraz w
klientach do uwierzytelniania wzglêdem serwerów.

GNU SASL zawiera bibliotekê (libgsasl), narzêdzie dzia³aj±ce z linii
poleceñ (gsasl) pozwalaj±ce na korzystanie z biblioteki z poziomu
pow³oki oraz dokumentacjê. Biblioteka ma obs³ugê szkieletu SASL (z
funkcjami uwierzytelniaj±cymi oraz zapewniaj±cymi prywatno¶æ i
spójno¶æ danych aplikacji) oraz przynajmniej czê¶ciow± obs³ugê
mechanizmów CRAM-MD5, EXTERNAL, GSSAPI, ANONYMOUS, PLAIN, SECURID,
DIGEST-MD5, LOGIN, NTLM oraz KERBEROS_V5.

Biblioteka jest przeno¶na, poniewa¿ sama nie korzysta z komunikacji
sieciowej, pozostawiaj±c to wywo³uj±cej j± aplikacji. Biblioteka jest
elastyczna ze wzglêdu na u¿ywan± infrastrukturê uwierzytelniania,
poniewa¿ korzysta z callbacków w aplikacji przy decydowaniu, czy
u¿ytkownik jest autoryzowany.

%package devel
Summary:	Header files for GNU SASL library
Summary(pl):	Pliki nag³ówkowe biblioteki GNU SASL
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%{?with_gss:Requires:	gss-devel >= 0.0.0}
Requires:	libgcrypt-devel >= 1.1.42
Requires:	libidn-devel >= 0.1.0
%{?with_ntlm:Requires:	libntlm-devel >= 0.3.5}
%{?with_krbv5:Requires:	shishi-devel >= 0.0.0}
Obsoletes:	libgsasl-devel

%description devel
Header files for GNU SASL library.

%description devel -l pl
Pliki nag³ówkowe biblioteki GNU SASL.

%package static
Summary:	Static GNU SASL library
Summary(pl):	Statyczna biblioteka GNU SASL
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	libgsasl-static

%description static
Static GNU SASL library.

%description static -l pl
Statyczna biblioteka GNU SASL.

%prep
%setup -q
%patch0 -p1

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
	--enable-gtk-doc \
	%{!?with_gss:--disable-gssapi} \
	%{!?with_krbv5:--disable-kerberos_v5} \
	%{!?with_ntlm:--disable-ntlm} \
	%{!?with_static_libs:--disable-static} \
	--with-html-dir=%{_gtkdocdir} \
	--with-libgcrypt

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

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
%{_mandir}/man1/gsasl.1*
%{_infodir}/*.info*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgsasl.so
%{_libdir}/libgsasl.la
%{_includedir}/gsasl*.h
%{_pkgconfigdir}/libgsasl.pc
%{_mandir}/man3/*.3*
%{_gtkdocdir}/gsasl

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgsasl.a
%endif
