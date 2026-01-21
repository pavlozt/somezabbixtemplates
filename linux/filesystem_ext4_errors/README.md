# Linux EXT4 Errors Guard


## Overview

Automatically monitors all mounted EXT4 filesystems for critical errors.
Template use files with mask `/sys/fs/ext4/*/errors_count`.

Usually in Zabbix another trigger fires earlier (Linux: FS [{#FSNAME}]: Filesystem has become read-only), but sometimes this one is needed.

This solution not will work with other filesystems like ZFS.

## Macros used

 no macros used.

## Discovery rules
 Automatic discovery all mounted ext4 filesystems

## Triggers

`Linux: FS errors on [{#FSNAME}]`