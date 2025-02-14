# To update dfhack to a new release, first run "prepare-dfhack-release RELEASE"
# where RELEASE is the upstream "dfversion-hackrelease" string. e.g. 0.44.05-r1.
# This gets the right submodule commits (which should be pasted below) and
# generates Source3 (git-describe.h).

# Autogenerate commit lines from prepare-dfhack-release:

# dfhack submodule: depends/clsocket
%global commit10 8340c07802078d905e60e294211a1807ec6f0161
# dfhack submodule: depends/jsoncpp-sub
%global commit11 ddabf50f72cf369bf652a95c4d9fe31a1865a781
# dfhack submodule: library/xml
%global commit12 0792fc0202fb6a04bfdaa262bc36a3b14c8581e5
# dfhack submodule: plugins/isoworld
%global commit13 e3c49ab017da2dcbeaadccd10e56d07d8f03b4ca
# dfhack submodule: plugins/isoworld/agui
#global commit14 1bd1b32083a62b4b851c81d41cceb4e5be6d08b4
# dfhack submodule: plugins/isoworld/allegro
#global commit15 8f4dd2f4a9a3d0028f903681a95e0587586ed0b1
# dfhack submodule: plugins/stonesense
%global commit14 b9fc28836f34f7ce1be64de94afd90184a341c7d
# dfhack submodule: scripts
%global commit15 2079b9fb69b8b4db48aa35ec54a96f5cca7cc8ef

# End autogenerated commit lines.

# Shortcommits:
%global shortcommit10 %(c=%{commit10}; echo ${c:0:7})
%global shortcommit11 %(c=%{commit11}; echo ${c:0:7})
%global shortcommit12 %(c=%{commit12}; echo ${c:0:7})
%global shortcommit13 %(c=%{commit13}; echo ${c:0:7})
%global shortcommit14 %(c=%{commit14}; echo ${c:0:7})
%global shortcommit15 %(c=%{commit14}; echo ${c:0:7})

# dfhack version string.
%global dfversion 0.47.04
%global hackrelease r1

# Define dfhack build architecture.
%global dfhack_arch 32
%ifarch x86_64
%global dfhack_arch 64
%endif

# Use old cmake macro
%global __cmake_in_source_build 1

Name:           dfhack
Version:        %{dfversion}
Release:        13.%{hackrelease}%{?dist}
Summary:        Memory hacking library for Dwarf Fortress and a set of tools that use it

# It'd be nice if we could unbundle some of these things, but I suspect it won't happen.
# Licensing explained in LICENSE.rst quite thoroughly, though. Thanks upstream!
License:        zlib and MIT and BSD and CC-BY-SA
URL:            https://github.com/DFHack/dfhack

# Main dfhack archive.
Source0:        https://github.com/DFHack/dfhack/archive/%{dfversion}-%{hackrelease}/dfhack-%{dfversion}-%{hackrelease}.tar.gz

# Script to actually *run* dfhack, adapted from Arch.
# (gets installed as "dfhack-run", "dfhack", and "dwarffortress-hacked").
Source1:        dfhack-run

# pkgconfig file for other plugins to use.
Source2:        dfhack.pc.in

# Git describe header, generated by prepare-dfhack-release script.
Source3:        git-describe.h

# prepare-dfhack-release script.
Source4:        prepare-dfhack-release

# Submodules. I started at 10, as there are some loose source files too.
# See https://github.com/DFHack/dfhack/blob/master/.gitmodules
Source10:       https://github.com/DFHack/clsocket/archive/%{commit10}/dfhack-clsocket-%{shortcommit10}.tar.gz
Source11:       https://github.com/open-source-parsers/jsoncpp/archive/%{commit11}/dfhack-jsoncpp-%{shortcommit11}.tar.gz
Source12:       https://github.com/DFHack/df-structures/archive/%{commit12}/dfhack-df-structures-%{shortcommit12}.tar.gz
Source13:       https://github.com/DFHack/isoworld/archive/%{commit13}/dfhack-isoworld-%{shortcommit13}.tar.gz
Source14:       https://github.com/DFHack/stonesense/archive/%{commit14}/dfhack-stonesense-%{shortcommit14}.tar.gz
Source15:       https://github.com/DFHack/scripts/archive/%{commit15}/dfhack-scripts-%{shortcommit15}.tar.gz

# Patch to unbundle Agui from dfhack-plugins-isoworld.
# We're not building isoworld at the moment.
#Patch0:         isoworld-external-allegro-agui.patch

# Patch to include cmath in isoworld.
# Patch1:         isoworld-cmath-include.patch

# See https://github.com/DFHack/dfhack/issues/961 for these isoworld issues.

# Patch to make protobuf build on F33/F32 with gcc 10.
# https://github.com/DFHack/dfhack/issues/1506
Patch3:         protobuf-gcc-10-fix.patch
# https://github.com/DFHack/dfhack/commit/39c650de131f85ea74d1f7638c3ea630faed5c15
Patch4:         %{name}-0.47.05-fpermissive-uicommon.patch

# dfhack only supports DF architectures, of which there are two.
ExclusiveArch:  %{ix86} x86_64

BuildRequires:  gcc, git, cmake, zlib-devel, mesa-libGL-devel
BuildRequires:  perl-XML-LibXML, perl-XML-LibXSLT, perl-Digest-SHA, perl-File-Copy
BuildRequires:  gcc-c++

# I think this is necessary now, otherwise the build fails.
BuildRequires:  SDL-devel

# Unbundled ruby.
BuildRequires:  ruby-libs, ruby-devel
Requires:       ruby, ruby-libs, ruby-devel

# For stonesense and isoworld.
%if 0%{?fedora}
BuildRequires:  allegro5-devel, allegro5-addon-ttf-devel, allegro5-addon-image-devel,
BuildRequires:  allegro5-addon-dialog-devel
%endif

# Unbundled tinyxml.
BuildRequires:  tinyxml-devel

Requires:       dwarffortress, valgrind

# List of bundled provides... dfhack currently provides _no_ way to not bundle these.
# Also, they have been modified downstream inside the dfhack tree.
Provides:       bundled(tinythread) = 1.1
Provides:       bundled(jsoncpp) = 1.6.5
Provides:       bundled(lua) = 5.3.3
# This was unbundled, but because dfhack and df must be built / are built with D_GLIBCXX_USE_CXX11_ABI=0
# it currently doesn't work. When df upstream is built against gcc >= 5.0, this can be unbundled.
Provides:       bundled(tinyxml) = 2.5.3

# Protobuf is forked, but the last version was 2.4.1, so... use that.
Provides:       bundled(protobuf) = 2.4.1

%description
DFHack is a Dwarf Fortress memory access library, distributed with a wide
variety of useful scripts and plugins.

For users, it provides a significant suite of bugfixes and interface
enhancements by default, and more can be enabled. There are also many tools
(such as workflow or autodump) which can make life easier. You can even add
third-party scripts and plugins to do almost anything!

For modders, DFHack makes many things possible. Custom reactions, new
interactions, magic creature abilities, and more can be set through Scripts
for Modders and custom raws. Non-standard DFHack scripts and inits can be
stored in the raw directory, making raws or saves fully self-contained for
distribution - or for coexistence in a single DF install, even with
incompatible components.

For developers, DFHack unites the various ways tools access DF memory and
allows easier development of new tools. As an open-source project under
various copyleft licenses, contributions are welcome.

# Spit out a -devel subpackage containing include files for all
# dependencies.
%package devel

Summary:  Development files and headers for dfhack

# Require dfhack, dfhack-static
Requires: %{name}%{?_isa} = %{version}-%{release}

# Provide the static package.
Provides: dfhack-static = %{version}-%{release}

%description devel

This package contains the development headers and files necessary
to build dfhack plugins.

# Generate a doc subpackage for the noarch documentation.
%package doc

Summary:        DFHack documentation
BuildArch:      noarch

%description doc

This package contains the documentation for dfhack, a Dwarf Fortress
memory access library and API. See the description of the "dfhack"
package for more information.

# Plugin subpackages.
# At the moment, that's just stonesense, but isoworld (when we figure out how to build it)
# or any other 'large' dfhack plugins should be included here.

# If for some reason a plugin should be shipped independently of dfhack this is, I guess,
# a template for how to do it, either as a subpackage or a separate package.
# (Though the latter is probably currently almost impossible to build).

%if 0%{?fedora}

%package plugin-stonesense

Summary:   A retro isometric visualizer for Dwarf Fortress

# Require dfhack.
Requires: %{name}%{?_isa} = %{version}-%{release}

# Provide "stonesense"; the software is commonly called that.
# also more importantly, there is discussion about splitting stonesense out of dfhack
# meaning it would need to be packaged separately.
Provides:  stonesense = %{version}-%{release}

%description plugin-stonesense

Stonesense is a third party visualizer that lets you view your Dwarf
Fortress world in a classic isometric perspective. It is implemented as
a plugin for dfhack.

%endif

%prep
%setup -qn dfhack-%{dfversion}-%{hackrelease}

# Extract submodules onto the right place.
tar xfz %SOURCE10 -C depends/clsocket --strip-components=1
tar xfz %SOURCE11 -C depends/jsoncpp-sub --strip-components=1
tar xfz %SOURCE12 -C library/xml --strip-components=1
tar xfz %SOURCE13 -C plugins/isoworld --strip-components=1
tar xfz %SOURCE14 -C plugins/stonesense --strip-components=1
tar xfz %SOURCE15 -C scripts --strip-components=1

# Put git-describe.h in the right place.
cp -a %SOURCE3 library/include/

# Apply patches. This complains about line endings, for some reason...
# You know what, don't apply patches. We don't build isoworld, anyway.
#patch -P0 -p1
#patch -P1 -p1
%patch -P4 -p1

# Fix protobuf problem; there's probably a way to do this with the patch macro.
patch depends/protobuf/google/protobuf/message.cc %PATCH3

# Manually (for now) apply fix to plugins/stonesense/CMakeLists.txt.
sed 's/dfhack-tinyxml/${DFHACK_TINYXML}/' -i plugins/stonesense/CMakeLists.txt

# Fix an issue caught by -fpermissive in isoworld.
sed 's/MapSection::load_colors/load_colors/g' -i plugins/isoworld/MapSection.h

# Remove the bundled agui.
rm -rf plugins/isoworld/agui/

# Comment out piece of code that uses git-describe.
sed "s/ADD_DEPENDENCIES(dfhack-version git-describe)/#ADD_DEPENDENCIES(dfhack-version git-describe)/" -i library/CMakeLists.txt

%build
cd build
# cmake options
# * set install prefix to libdir/dfhack
# * build stonesense
# * link stonesense against system-wide allegro
# * link against system-wide tinyxml
# * don't download libruby.so, load system one.
%cmake .. -DCMAKE_BUILD_TYPE:string=Release -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_libdir}/dfhack -DDFHACK_BUILD_ARCH=%{dfhack_arch} %{?fedora:-DBUILD_STONESENSE:BOOL=True -DSTONESENSE_INTERNAL_SO=OFF} -DDOWNLOAD_RUBY=OFF
# These do not seem to work currently.
# -DBUILD_ISOWORLD=ON -DISOWORLD_INTERNAL_SO=OFF
%make_build

# Create pkgconfig file.
sed -e 's,@version@,%{version}-%{hackrelease},' -e 's,@libdir@,%{_libdir},' -e 's,@prefix@,%{_prefix},' -e 's,@includedir@,%{_includedir},' < %SOURCE2 > dfhack.pc

%install
cd build/
make install

# Install the runner scripts, modify them appropriately.
mkdir -p %{buildroot}/%{_bindir}
install -m755 -p %SOURCE1 %{buildroot}%{_bindir}/
ln -s %{_bindir}/dfhack-run %{buildroot}%{_bindir}/dfhack
ln -s %{_bindir}/dfhack-run %{buildroot}%{_bindir}/dwarffortress-hacked
sed 's|prefix=/usr|prefix=%{_prefix}|' -i %{buildroot}%{_bindir}/dfhack-run
sed 's|libdir=lib|libdir=%{_libdir}|' -i %{buildroot}%{_bindir}/dfhack-run


# Move data out of "_libdir/dfhack" and into "_datadir/dfhack".
mkdir -p %{buildroot}%{_datadir}/dfhack
mv %{buildroot}%{_libdir}/dfhack/dfhack.init-example %{buildroot}%{_datadir}/dfhack/
mv %{buildroot}%{_libdir}/dfhack/dfhack-config %{buildroot}%{_datadir}/dfhack/

# Stonesense data, too, should be in usr/share.
%if 0%{?fedora}
mv %{buildroot}%{_libdir}/dfhack/stonesense %{buildroot}%{_datadir}/dfhack/stonesense/
%endif

# Install the headers that are necessary.
mkdir -p %{buildroot}%{_includedir}/dfhack
mkdir -p %{buildroot}%{_includedir}/dfhack/dfhack
mkdir -p %{buildroot}%{_includedir}/dfhack/proto
mkdir -p %{buildroot}%{_includedir}/dfhack/lua
mkdir -p %{buildroot}%{_includedir}/dfhack/protobuf
cp -ar ../library/include/* %{buildroot}%{_includedir}/dfhack/dfhack/
cp -ar ../library/proto/*.proto ../library/proto/*.h %{buildroot}%{_includedir}/dfhack/proto/
cp -ar ../depends/lua/include/* %{buildroot}%{_includedir}/dfhack/lua/

# This one is harder, unfortunately.
cp -ar depends/protobuf/config.h %{buildroot}%{_includedir}/dfhack/protobuf/
cd ../depends/protobuf/
find google/ -name '*.h' -exec cp --parents \{\} %{buildroot}%{_includedir}/dfhack/protobuf/ \;
cd ../../build/

# Install the pkgconfig file.
mkdir -p %{buildroot}%{_libdir}/pkgconfig/
cp -a dfhack.pc %{buildroot}%{_libdir}/pkgconfig/

# Install static libraries for plugins to link with.
cp library/libdfhack-version.a %{buildroot}%{_libdir}/dfhack/hack/

# Fix executable flag on some protobuf files.
chmod -x %{buildroot}%{_includedir}/dfhack/proto/*.proto

# Exclude docs build script.
rm -f docs/build.sh

%if 0%{?fedora}
%files plugin-stonesense
%{_libdir}/dfhack/hack/plugins/stonesense.plug.so
%{_datadir}/dfhack/stonesense/
%doc plugins/stonesense/README.md plugins/stonesense/docs
%license plugins/stonesense/LICENSE
%endif

%files devel
%exclude %{_includedir}/dfhack/dfhack/df/.gitignore
%{_includedir}/dfhack/
%{_libdir}/pkgconfig/dfhack.pc
%{_libdir}/dfhack/hack/libdfhack-version.a

%files doc
%doc docs/*
%license LICENSE.rst

%files
%if 0%{?fedora}
%exclude %{_datadir}/dfhack/stonesense
%exclude %{_libdir}/dfhack/hack/plugins/stonesense.plug.so
%endif
%exclude %{_libdir}/dfhack/hack/libdfhack-version.a
%{_bindir}/dfhack
%{_bindir}/dfhack-run
%{_bindir}/dwarffortress-hacked
%{_libdir}/dfhack/
%{_datadir}/dfhack/
%doc README.md
%license LICENSE.rst

%changelog
* Wed Jan 29 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.47.04-13.r1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Aug 02 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.47.04-12.r1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Feb 04 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.47.04-11.r1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Aug 03 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.47.04-10.r1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Aug 08 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.47.04-9.r1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Thu Apr 14 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.47.04-8.r1
- Backport upstream fix to compile with -fpermissive for uicommon.h

* Thu Feb 10 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.47.04-7.r1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Aug 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.47.04-6.r1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Apr 25 2021 Leigh Scott <leigh123linux@gmail.com> - 0.47.04-5.r1
- Rebuilt for removed libstdc++ symbol (#1937698)

* Thu Feb 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.47.04-4.r1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Aug 19 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.47.04-3.r1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jun 18 2020 Ben Rosser <rosser.bjr@gmail.com> - 0.47.04-2.r1
- Update to stable release with support for 0.47.04.

* Mon Apr 20 2020 Ben Rosser <rosser.bjr@gmail.com> - 0.47.04-1.beta1
- Update to latest upstream release with support for 0.47.04.

* Mon Feb 24 2020 Ben Rosser <rosser.bjr@gmail.com> - 0.47.03-1.alpha0
- Update to latest upstream release with support for 0.47.03.

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.44.12-6.r2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Aug 10 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.44.12-5.r2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Mar 27 2019 Ben Rosser <rosser.bjr@gmail.com> - 0.44.12-4.r2
- Fix FTBFS in Stonesense on Fedora 30 and up.

* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.44.12-3.r2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 08 2019 Ben Rosser <rosser.bjr@gmail.com> - 0.44.12-2.r2
- Updated to latest upstream release for 0.44.12.

* Sat Dec 01 2018 Ben Rosser <rosser.bjr@gmail.com> - 0.44.12-1.r1
- Updated to latest upstream release for 0.44.12.
- Add new submodule for jsoncpp.

* Sun Aug 19 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.44.10-3.r1
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <sergio@serjux.com> - 0.44.10-2.r1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 04 2018 Ben Rosser <rosser.bjr@gmail.com> - 0.44.10-1.r1
- Updated to latest upstream release for 0.44.10.

* Mon Apr 09 2018 Ben Rosser <rosser.bjr@gmail.com> - 0.44.09-1.r1
- Update to latest upstream release for 0.44.09.

* Mon Feb 26 2018 Ben Rosser <rosser.bjr@gmail.com> - 0.44.05-3.r2
- Update to latest upstream release for 0.44.05.

* Wed Feb 21 2018 Ben Rosser <rosser.bjr@gmail.com> - 0.44.05-2.r1
- Added missing provides for dfhack-static to dfhack-devel.

* Tue Feb 20 2018 Ben Rosser <rosser.bjr@gmail.com> - 0.44.05-1.r1
- Update to latest upstream release, add various review fixes.
- Remove static subpackage, move static library into devel subpackage.
- Remove re-definition of dist tag for EPEL.
- Use make_build instead of make smp_flags macro.
- Remove BR on git.
- Add comment to upstream ticket about isoworld issues/patches.
- Generate dfhack-doc subpackage, excluding documentation build script.

* Sun Dec 31 2017 Ben Rosser <rosser.bjr@gmail.com> - 0.44.03-1.beta1
- Updated to latest dfhack upstream release, beta1 for 0.44.03.
- Redid packaging to use several source URLs, one for each git repository.
- Commit hashes and git-describe.h get generated by prepare-dfhack-release,
  script, both included in source RPM.
- Fixed executable permissions on some proto files, excluded df-structures
  gitignore in devel package.
- Added bundled protobuf version to Provide.
- Made stonesense Provides versioned.

* Sun Jul 16 2017 Ben Rosser <rosser.bjr@gmail.com> - 0.43.05-7.r2
- Update to latest dfhack upstream release, r2 for 0.43.05.

* Tue Jun 20 2017 Ben Rosser <rosser.bjr@gmail.com> - 0.43.05-6.r1
- Update to r1 release for DF 0.43.05.

* Tue May 09 2017 Ben Rosser <rosser.bjr@gmail.com> - 0.43.05-5.beta2
- Update to beta2 release for DF 0.43.05.

* Wed Feb 15 2017 Ben Rosser <rosser.bjr@gmail.com> - 0.43.05-4.beta1
- Update to beta1 release for DF 0.43.05.

* Fri Jan 20 2017 Ben Rosser <rosser.bjr@gmail.com> - 0.43.05-3.alpha4
- Rebuild with DOWLOAD_RUBY actually set to off.

* Fri Jan 20 2017 Ben Rosser <rosser.bjr@gmail.com> - 0.43.05-2.alpha4
- Update to latest 0.43.05 alpha release.
- The libruby.so symlink is no longer required.

* Sun Oct 23 2016 Ben Rosser <rosser.bjr@gmail.com> - 0.43.05-1.alpha1
- Initial support for 0.43.05 and 64-bit Dwarf Fortress; not perfectly stable.
- Now that ruby plugin supports 2.x libruby, unbundle libruby.
- Rebundle tinyxml; as dfhack segfaults when it is unbundled for whatever reason.
- Keep libdfhack-version as static library, install it in dfhack-static package.

* Sat Oct 1 2016 Ben Rosser <rosser.bjr@gmail.com> - 0.43.03-6.r1
- Add -devel subpackage containing all development headers and pkgconfig file.
- Build libdfhack-version as shared library and install it in main package.

* Thu Jul 7 2016 Ben Rosser <rosser.bjr@gmail.com> 0.43.03-5.r1
- Update to 0.43.03 stable release
- Unbundle tinyxml, link against system-wide tinyxml (patch accepted upstream)

* Sat Jun 18 2016 Ben Rosser <rosser.bjr@gmail.com> 0.43.03-4.alpha1
- Unbundle allegro, link stonesense against system-wide allegro.

* Sat Jun 18 2016 Ben Rosser <rosser.bjr@gmail.com> 0.43.03-3.alpha1
- Fix bug in dfhack-run when installing stonesense.

* Sat Jun 18 2016 Ben Rosser <rosser.bjr@gmail.com> 0.43.03-2.alpha1
- Change Source0 to use version macro so I don't accidentally forget to update it.

* Sat Jun 18 2016 Ben Rosser <rosser.bjr@gmail.com> 0.43.03-1.alpha1
- Update to 0.43.03 alpha release

* Fri Jun 17 2016 Ben Rosser <rosser.bjr@gmail.com> 0.42.06-2.r1
- Switch to using _libdir and _datadir to store dfhack instead of opt.
- Added valgrind as run-time dependency.
- Include stonesense as subpackage.

* Fri Jun 17 2016 Ben Rosser <rosser.bjr@gmail.com> 0.42.06-1.r1
- Initial package.
