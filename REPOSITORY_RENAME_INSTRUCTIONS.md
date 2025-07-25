# Repository Rename Instructions

## Manual Repository Rename Steps

Since the GitHub CLI is not available, you'll need to rename the repository manually through the GitHub web interface:

### Steps to Rename Repository:

1. **Go to GitHub Repository**:
   - Navigate to: https://github.com/hunter-admin/stamp-card-manager

2. **Access Repository Settings**:
   - Click on the "Settings" tab at the top of the repository page

3. **Rename Repository**:
   - Scroll down to the "Repository name" section
   - Change the name from `stamp-card-manager` to `redcat-stamp-card-manager`
   - Click "Rename" button

4. **Update Local Git Remote** (after GitHub rename):
   ```bash
   git remote set-url origin https://github.com/hunter-admin/redcat-stamp-card-manager.git
   ```

### Alternative: Use GitHub CLI (if available):
```bash
gh repo rename redcat-stamp-card-manager
```

## Changes Already Completed ✅

The following cleanup tasks have been completed and committed:

- ✅ **Removed Branding Assets**: Deleted SCM.ico and SCM.png files
- ✅ **Updated Build Configuration**: Removed icon references from build.spec
- ✅ **Updated Application Name**: Changed executable name to RedcatStampCardManager
- ✅ **Cleaned Configuration**: Updated config.json with generic business settings
- ✅ **Updated Documentation**: Modified README.md to reflect new repository name
- ✅ **Removed Brand References**: Cleaned up all example configurations

## Repository Status

- **Current Name**: stamp-card-manager
- **Target Name**: redcat-stamp-card-manager
- **Owner**: hunter-admin
- **All branding cleanup**: ✅ Complete
- **Ready for rename**: ✅ Yes

The repository is now completely unbranded and ready for the rename operation.