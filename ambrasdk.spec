# for compatibility with old md5 digest
# %global _binary_filedigest_algorithm 1
# %global _source_filedigest_algorithm 1

%define defaultbuildroot /
# Do not try autogenerate prereq/conflicts/obsoletes and check files
%undefine __check_files
%undefine __find_prereq
%undefine __find_conflicts
%undefine __find_obsoletes
# Be sure buildpolicy set to do nothing
%define __spec_install_post %{nil}
# Something that need for rpm-4.1
%define _missing_doc_files_terminate_build 0

%define name    ambra-sdk
%define version 3.20.3.0

Summary: Ambra-SDK library
Name: %{name}
Version: %{version}
Release: 4
License: Apache-2.0
Group: dicomgrid
BuildArch: noarch
AutoReqProv: no

%description
Ambra SDK
