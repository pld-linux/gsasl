#
# Conditional build:
%bcond_without	gss	# without GSSAPI mechanism
%bcond_without	krbv5	# without KERBEROS_V5 mechanism
%bcond_without	ntlm	# without NTLM mechanism
#
Summary:	GNU SASL - implementation of the Simple Authentication and Security Layer
Summary(pl):	GNU SASL - implementacja Simple Authentication and Security Layer
Name:		gsasl
Version:	0.1.3
Release:	1
License:	GPL
Group:		Libraries
Source0:	http://josefsson.org/gsasl/releases/%{name}-%{version}.tar.gz
# Source0-md5:	bd902e2a88e03720557d72c44131dee0
Source1:	%{name}-pl.po
Source2:	%{name}-lib-pl.po
Patch0:		%{name}-info.patch
URL:		http://www.gnu.org/software/gsasl/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1.8
BuildRequires:	gettext-devel >= 0.14.1
%{?with_gss:BuildRequires:	gss-devel >= 0.0.0}
BuildRequires:	gtk-doc >= 1.1
BuildRequires:	libgcrypt-devel >= 1.1.42
BuildRequires:	libidn-devel >= 0.1.0
%{?with_ntlm:BuildRequires:	libntlm-devel >= 0.3.1}
BuildRequires:	libtool >= 2:1.5
# alternatively, krb5 or heimdal could be used for GSSAPI and KERBEROS_V5
%{?with_krbv5:BuildRequires:	shishi-devel >= 0.0.0}
BuildRequires:	texinfo
Requires(post,postun):	/sbin/ldconfig
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
%{?with_ntlm:Requires:	libntlm-devel >= 0.3.1}
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

cp -f %{SOURCE1} po/pl.po
cp -f %{SOURCE2} lib/po/pl.po
echo 'pl' >> po/LINGUAS
echo 'pl' >> lib/po/LINGUAS
rm -f po/stamp-po lib/po/stamp-po

# incompatible with ksh
rm -f m4/libtool.m4

%build
# blegh, lt incompatible with ksh - must rebuild
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_gss:--disable-gssapi} \
	%{!?with_krbv5:--disable-kerberos_v5} \
	%{!?with_ntlm:--disable-ntlm} \
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# libgsasl for lib, gsasl for app
%find_lang %{name} --all-name

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
%{_includedir}/gsasl.h
%{_pkgconfigdir}/libgsasl.pc
%{_mandir}/man3/*.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libgsasl.a
