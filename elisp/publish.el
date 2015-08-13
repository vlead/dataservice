;;; org-publish.el

;;; Adapted from Sebastian Rose's org publishing tutorial at
;;; http://orgmode.org/worg/org-tutorials/org-publish-html-tutorial.html

;;; Customized for use by vlead-system team.

;; Maintainer: Venkatesh Choppella <venkatesh.choppell@iiit.ac.in>
;;  VLEAD  <engg@vlabs.ac.in>
;; Keywords: publish, org

;; It is released under the same terms, namely the GPL v2 or
;; later.

;; This software is distributed in the hope that it will be
;; useful, but WITHOUT ANY WARRANTY; without even the
;; implied warranty of MERCHANTABILITY or FITNESS FOR A
;; PARTICULAR PURPOSE.  See the GNU General Public License
;; for more details.

;; You should have received a copy of the GNU General Public License
;; along with GNU Emacs; see the file COPYING.  If not, write to the
;; Free Software Foundation, Inc., 59 Temple Place - Suite 330,
;; Boston, MA 02111-1307, USA.

;;; Usage:
;;; This file is loaded by the docs target of the
;;; makefile in the parent directory.

;;; Requirements:
;;; make sure that org-8.2.10 is available at
;;; ~/emacs/lisp/org-8.2.10.

(setq load-path
      (append
       (list "~/emacs/lisp/org-8.2.10/lisp"
	     "~/emacs/lisp/org-8.2.10/contrib/lisp")
       load-path))

(require 'org)
(require 'ob-tangle)
(load-file "./elisp/tangle-with-publish-dir.el")

(message "Org version = %s" (org-version))
(message "Org version = %s" (org-version))
(message "Org version = %s" (org-version))
(message "load-path = %s" load-path)

(setq org-export-allow-BIND t)
;;; tangle code before publishing
(add-hook 'org-publish-before-export-hook 'org-babel-tangle 'append)
;(add-hook 'org-publish-before-export-hook 'org-babel-tangle)

;(setq org-babel-default-header-args
;      (cons '(:mkdirp . "yes")
;	    ;;; if mkdirp is already there, delete it
;	    (assq-delete-all :mkdirp org-babel-default-header-args)))

(setq org-babel-default-header-args
      (append '((:eval . "no") (:mkdirp . "yes"))
	    ;;; if mkdirp is already there, delete it
	    ;;; if eval is already there, delete it
	    ;;; if org-src-preserve-indentation is already there, delete it
	    (progn
	      (assq-delete-all :mkdirp  org-babel-default-header-args)
	      (assq-delete-all :eval    org-babel-default-header-args))))


;;; https://groups.google.com/forum/#!topic/comp.emacs/iiYJL04M7lA
;;; eliminate annoying messages from emacs about following
;;; version controlled files that are symlinks.
(setq vc-follow-symlinks t)

; Preserve whitespace indentation for .yml files!!
(setq org-src-preserve-indentation t)


;;; default-directory :: emacs defined variable.  Is equal
;;; to the directory from where the emacs is launched.

;;; base-dir :: equal to default-dir
;;; src-dir   =  base-dir/src
;;; build-dir =  base-dir/build
;;; docs-dir  =  build-dir/docs
;;; code-dir  =  build-dir/code

;;; CUSTOMIZE these variables!
(defvar *base-dir*  default-directory)
(defvar *src-dir*   (concat *base-dir* "src/"))
(defvar *build-dir* (concat *base-dir* "build/"))
(defvar *docs-dir*  (concat *build-dir* "docs/"))
(defvar *code-dir*  (concat *build-dir* "code/"))

(defvar org-docs '())
(defvar org-static '())
(defvar org-code '())
(defvar snag '())

(message "======================")
(message "base dir = %s" *base-dir*)
(message "docs dir= %s" *docs-dir*)
(message "code dir= %s" *code-dir*)

;(message "tangle func= %s" org-babel-tangle)
;(message "publish func= %s" org-html-publish-to-html)
(message "======================")
(interactive "press enter.....")

(defun tangle-wrapper (plist filename pub-dir)
  (org-babel-tangle-file/publish-dir filename pub-dir))


(setq org-code
`("org-code"
 :base-directory ,*src-dir*
 :base-extension "org"
 :publishing-directory ,*code-dir*
 :recursive t
 :publishing-function tangle-wrapper
  ))

(setq org-tangled `("org-tangled"
  :base-directory ,*src-dir*
  :base-extension "yml\\|yaml"
  :publishing-directory ,*code-dir*
  :recursive t
  :publishing-function org-publish-attachment
  ))


(setq org-docs
`("org-docs"
 :base-directory ,*src-dir*
 :base-extension "org"
 :publishing-directory ,*docs-dir*
 :recursive t
 :publishing-function org-html-publish-to-html
 :headline-levels 4             ; Just the default for this project.
 :auto-preamble t
 :auto-sitemap t
  ))

(setq org-static `("org-static"
  :base-directory ,*src-dir*
  :base-extension "css\\|js\\|png\\|ico\\|jpg\\|png\\|gif\\|mp3\\|ogg\\|swf\\|emacs\\|sh\\|py\\|pdf\\|tex\\|css\\|ss\\|rkt\\|flv\\|tgz"
  :publishing-directory ,*docs-dir*
  :recursive t
  :publishing-function org-publish-attachment
  ))

(setq snag
      '("snag" :components ("org-code" "org-docs"
      "org-static" "org-tangled")))

(require 'ox-publish)
(load-file "./elisp/htmlize.el")

(setq org-publish-project-alist
      (list org-code org-docs org-static org-tangled snag))

(org-publish-project
 snag  ; project name
 t ; force
 )

