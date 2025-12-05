# Linux EXT4 Errors Guard


## Overview

Automatically monitors all mounted EXT4 filesystems for critical errors.
Template use files with mask `/sys/fs/ext4/*/errors_count`.

This not will work with ZFS, etc.

## Macros used

 no macros used.

## Discovery rules
 Automatic discovery all mounted ext4 filesystems

## Triggers

`Linux: FS errors on [{#FSNAME}]`