BuildArch: x86_64
BuildRequires: tar, zstd
License: GPLv2 and Redistributable, no modification permitted
Name: kernel-hardened
Provides: installonlypkg(kernel-hardened)
Release: 1%{?dist}
Source0: https://mirror.sunred.org/archlinux/extra/os/x86_64/linux-hardened-6.6.8.hardened1-1-x86_64.pkg.tar.zst
Summary: The hardened linux kernel
URL: https://github.com/d4rklynk/kernel-hardened
Version: 6.6.8.1

%description
The hardened Linux kernel; originally from the Arch Linux repository and repackaged for Fedora Linux

%prep
# Define RPM macro(s) for the specified paths
%define _dnfconf %{_sysconfdir}/dnf/dnf.conf
%define _libmodules %{_prefix}/lib/modules

# Define RPM macro for the name of the directory containing the compiled kernel and its modules
%define _kerneldir 6.6.8-hardened1-1-hardened

# Define RPM macro for the number of levels to use when extracting the kernel directory from %SOURCE0
%define _tarstrip 3

%install
# Create the /usr/lib/modules directory within %buildroot
%{__mkdir} -p %{buildroot}%{_libmodules}

# Change directory
cd %{buildroot}%{_libmodules}

# Uncompress the kernel archive
%{__tar} --use-compress-program=unzstd -x -f %{SOURCE0} --strip %{_tarstrip}

%post
# Generate the initramfs image within /boot as well as the conf file for /boot/loader/entries
kernel-install add %{_kerneldir} %{_libmodules}/%{_kerneldir}/vmlinuz

# Check if the following option exists within dnf.conf. This option is responsible for keeping X number of previous versions for the given package, where X is defined by the 'installonly_limit' option (3 by default)
installonlypkgs="$(%{__grep} 'installonlypkgs' %{_dnfconf})";

# If the line does not exist, then add it with a comment
if [ -z "${installonlypkgs}" ]; then
  echo "# The following line was added by the 'kernel-hardened' package from Hard Hat OS (HOS)" >> %{_dnfconf};
  echo 'installonlypkgs=kernel-hardened' >> %{_dnfconf};
else
  # If the line already exists, then check if the package name has already been added
  already_added="$(echo ${installonlypkgs} | %{__grep} 'kernel-hardened')";
  # Check if the variable is empty. If so, then the package name will need to be added
  if [ -z "${already_added}" ]; then
    # Add the package name if it doesn't already exist for this option
    %{__sed} -i s/"${installonlypkgs}"/"${installonlypkgs} kernel-hardened"/g %{_dnfconf};
  fi;
fi;

%postun
# Prior to uninstalling the kernel, remove associated files from /boot
kernel-install remove %{_kerneldir}

# Display an informational message to stdout that this package has modified the dnf.conf file
echo -e "\nINFO: The %{_dnfconf} file was modified to add/include this package, 'kernel-hardened', to the option 'installonlypkgs'. Keeping this line will not harm your system, but you can remove it as it's no longer needed."

%files
%{_libmodules}/%{_kerneldir}
