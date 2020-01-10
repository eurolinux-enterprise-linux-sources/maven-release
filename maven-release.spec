Name:           maven-release
Version:        2.2.1
Release:        11%{?dist}
Summary:        Release a project updating the POM and tagging in the SCM

Group:          Development/Libraries
License:        ASL 2.0
URL:            http://maven.apache.org/plugins/maven-release-plugin/
Source0:        http://repo1.maven.org/maven2/org/apache/maven/release/%{name}/%{version}/%{name}-%{version}-source-release.zip
# Remove deps needed for tests, till jmock gets packaged
Patch1:         002-mavenrelease-fixbuild.patch
Patch2:         003-fixing-migration-to-component-metadata.patch

BuildArch:      noarch

BuildRequires:  java-devel
BuildRequires:  jpackage-utils
BuildRequires:  maven-local
BuildRequires:  maven-scm-test
BuildRequires:  maven-antrun-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-source-plugin
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-plugin-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-site-plugin
BuildRequires:  maven-plugin-testing-harness
BuildRequires:  plexus-containers-component-metadata
BuildRequires:  plexus-utils
BuildRequires:  maven-surefire-maven-plugin
BuildRequires:  maven-enforcer-plugin
BuildRequires:  jaxen


%description
This plugin is used to release a project with Maven, saving a lot of 
repetitive, manual work. Releasing a project is made in two steps: 
prepare and perform.


%package manager
Summary:        Release a project updating the POM and tagging in the SCM
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description manager
This package contains %{name}-manager needed by %{name}-plugin.


%package plugin
Summary:        Release a project updating the POM and tagging in the SCM
Group:          Development/Libraries
Requires:       %{name}-manager = %{version}-%{release}

%description plugin
This plugin is used to release a project with Maven, saving a lot of
repetitive, manual work. Releasing a project is made in two steps:
prepare and perform.


%package javadoc
Summary:        Javadocs for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}
Obsoletes:      %{name}-manager-javadoc <= 2.0-1
Obsoletes:      %{name}-plugin-javadoc <= 2.0-1

%description javadoc
This package contains the API documentation for %{name}.


%prep
%setup -q -n %{name}-%{version}

%patch1 -p1
%patch2 -p1

# Jmock and mockito are not present
%pom_remove_dep jmock:
%pom_remove_dep jmock: maven-release-plugin
%pom_remove_dep jmock: maven-release-manager
%pom_remove_dep org.mockito: maven-release-manager

cat > README << EOT
%{name}-%{version}

This plugin is used to release a project with Maven, saving a lot of
repetitive, manual work. Releasing a project is made in two steps:
prepare and perform.
EOT

%mvn_file ":%{name}-{*}" %{name}-@1

%mvn_package :maven-release maven-release
%mvn_package ":maven-release-{*}" maven-release-@1


%build
# Skip tests because we don't have dependencies (jmock)
%mvn_build -f

%install
%mvn_install

%files -f .mfiles-maven-release
%doc README LICENSE NOTICE

%files manager -f .mfiles-maven-release-manager
%doc LICENSE NOTICE

%files plugin -f .mfiles-maven-release-plugin
%doc LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE


%changelog
* Mon Aug 26 2013 Michal Srb <msrb@redhat.com> - 2.2.1-11
- Migrate away from mvn-rpmbuild (Resolves: #997504)

* Tue Jul 30 2013 Tomas Radej <tradej@redhat.com> - 2.2.1-10
- Removed Jmock + mockito

* Wed Jul 17 2013 Tomas Radej <tradej@redhat.com> - 2.2.1-9
- Installed LICENSE and NOTICE

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.1-8
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.2.1-6
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Mon Sep 17 2012 Jaromir Capik <jcapik@redhat.com> - 2.2.1-5
- Fixing incomplete migration to component metadata

* Tue Aug  7 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.1-4
- Remove BR: maven-scm-test

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 29 2011 Alexander Kurtakov <akurtako@redhat.com> 2.2.1-1
- Update to latest upstream release.
- Adapt to current guidelines.

* Tue Jul 26 2011 Guido Grazioli <guido.grazioli@gmail.com> - 2.2-3
- Reinclude maven-scm-test in BRs

* Tue Jul 26 2011 Guido Grazioli <guido.grazioli@gmail.com> - 2.2-2
- Import patch provided by Jaromír Cápík (#725088)

* Mon Jul 18 2011 Guido Grazioli <guido.grazioli@gmail.com> - 2.2-1
- Update to 2.2
- Update to current guidelines
- Build with maven 3

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 3 2011 Alexander Kurtakov <akurtako@redhat.com> 2.0-2
- Drop tomcat5 BRs.
- Drop versioned jars.

* Mon Sep 13 2010 Guido Grazioli <guido.grazioli@gmail.com> - 2.0-1
- Update to upstream 2.0

* Sat Sep 11 2010 Guido Grazioli <guido.grazioli@gmail.com> - 2.0-0.659858svn.4
- Fix build requires
- Use javadoc:aggregate goal

* Tue May 25 2010 Guido Grazioli <guido.grazioli@gmail.com> - 2.0-0.659858svn.3
- Fix build requires

* Mon May 10 2010 Guido Grazioli <guido.grazioli@gmail.com> - 2.0-0.659858svn.2
- Fix release tag
- Better macro usage

* Mon Apr 26 2010 Guido Grazioli <guido.grazioli@gmail.com> - 2.0-0.659858svn.1
- Install maven-release-parent pom in dedicated package
- Patch maven-release-plugin to skip helpmojo goal
- Patch to skip tests depending on (unpackaged) jmock

* Fri Apr 16 2010 Guido Grazioli <guido.grazioli@gmail.com> - 2.0-0.659858svn
- Initial packaging
