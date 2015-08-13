;;;###autoload
(defun org-babel-tangle-file/publish-dir  (file &optional publish-dir target-file lang)
  "Extract the bodies of source code blocks in FILE.
Source code blocks are extracted with `org-babel-tangle'.
Optional argument TARGET-FILE can be used to specify a default
export file for all source blocks.  Optional argument LANG can be
used to limit the exported source code blocks by language.
Return a list whose CAR is the tangled file name."
  (interactive "fFile to tangle: \nP")
  (let ((visited-p (get-file-buffer (expand-file-name file)))
	to-be-removed)
    (prog1
	(save-window-excursion
	  (find-file file)
	  (setq to-be-removed (current-buffer))
	  (org-babel-tangle/publish-dir nil publish-dir target-file lang))
      (unless visited-p
	(kill-buffer to-be-removed)))))

;;;###autoload
(defun org-babel-tangle/publish-dir (&optional arg publish-dir target-file lang)
  "Write code blocks to source-specific files.
Extract the bodies of all source code blocks from the current
file into their own source-specific files.
With one universal prefix argument, only tangle the block at point.
When two universal prefix arguments, only tangle blocks for the
tangle file of the block at point.
Optional argument TARGET-FILE can be used to specify a default
export file for all source blocks.  Optional argument LANG can be
used to limit the exported source code blocks by language."
  (interactive "P")
  (run-hooks 'org-babel-pre-tangle-hook)
  ;; Possibly Restrict the buffer to the current code block
  (save-restriction
    (when (equal arg '(4))
      (let ((head (org-babel-where-is-src-block-head)))
	  (if head
	      (goto-char head)
	    (user-error "Point is not in a source code block"))))
    (save-excursion
      (let ((block-counter 0)
	    (org-babel-default-header-args
	     (if target-file
		 (org-babel-merge-params org-babel-default-header-args
					 (list (cons :tangle target-file)))
	       org-babel-default-header-args))
	    (tangle-file
	     (when (equal arg '(16))
	       (or (cdr (assoc :tangle (nth 2 (org-babel-get-src-block-info 'light))))
		   (user-error "Point is not in a source code block"))))
	    path-collector)
	(mapc ;; map over all languages
	 (lambda (by-lang)
	   (let* ((lang (car by-lang))
		  (specs (cdr by-lang))
		  (ext (or (cdr (assoc lang org-babel-tangle-lang-exts)) lang))
		  (lang-f (intern
			   (concat
			    (or (and (cdr (assoc lang org-src-lang-modes))
				     (symbol-name
				      (cdr (assoc lang org-src-lang-modes))))
				lang)
			    "-mode")))
		  she-banged)
	     (mapc
	      (lambda (spec)
		(let ((get-spec (lambda (name) (cdr (assoc name (nth 4 spec))))))
		  (let* ((tangle (funcall get-spec :tangle))
			 (she-bang (let ((sheb (funcall get-spec :shebang)))
                                     (when (> (length sheb) 0) sheb)))
			 (tangle-mode (funcall get-spec :tangle-mode))
			 (base-name (cond
				     ((string= "yes" tangle)
				      (file-name-sans-extension
				       (buffer-file-name)))
				     ((string= "no" tangle) nil)
				     ((> (length tangle) 0) tangle)))
			 (file-name (concat publish-dir 
					    (when base-name
					      ;; decide if we want to add ext to base-name
					      (if (and ext (string= "yes" tangle))
						  (concat base-name "." ext) base-name)))))
		    (when file-name
		      ;; Possibly create the parent directories for file.
		      (let ((m (funcall get-spec :mkdirp))
			    (fnd  (file-name-directory  file-name)))

			(message "==== fnd = %s" fnd)
			(message "==== fnd = %s" fnd)
			(message "==== fnd = %s" fnd)

			(and m fnd (not (string= m "no"))
			     (make-directory fnd 'parents)))


		      ;; delete any old versions of file
		      (and (file-exists-p file-name)
			   (not (member file-name (mapcar #'car path-collector)))
			   (delete-file file-name))
		      ;; drop source-block to file
		      (with-temp-buffer
			(when (fboundp lang-f) (ignore-errors (funcall lang-f)))
			(when (and she-bang (not (member file-name she-banged)))
			  (insert (concat she-bang "\n"))
			  (setq she-banged (cons file-name she-banged)))
			(org-babel-spec-to-string spec)
			;; We avoid append-to-file as it does not work with tramp.
			(let ((content (buffer-string)))
			  (with-temp-buffer
			    (message "file-name = %s" file-name)
			    (if (file-exists-p file-name)
				(insert-file-contents file-name))
			    (goto-char (point-max))
			    (insert content)
			    (write-region nil nil file-name))))
		      ;; if files contain she-bangs, then make the executable
		      (when she-bang
			(unless tangle-mode (setq tangle-mode #o755)))
		      ;; update counter
		      (setq block-counter (+ 1 block-counter))
		      (add-to-list 'path-collector
				   (cons file-name tangle-mode)
				   nil
				   (lambda (a b) (equal (car a) (car b))))))))
	      specs)))
	 (if (equal arg '(4))
	     (org-babel-tangle-single-block 1 t)
	   (org-babel-tangle-collect-blocks lang tangle-file)))
	(message "Tangled %d code block%s from %s" block-counter
		 (if (= block-counter 1) "" "s")
		 (file-name-nondirectory
		  (buffer-file-name
		   (or (buffer-base-buffer) (current-buffer)))))
	;; run `org-babel-post-tangle-hook' in all tangled files
	(when org-babel-post-tangle-hook
	  (mapc
	   (lambda (file)
	     (org-babel-with-temp-filebuffer file
	       (run-hooks 'org-babel-post-tangle-hook)))
	   (mapcar #'car path-collector)))
	;; set permissions on tangled files
	(mapc (lambda (pair)
		(when (cdr pair) (set-file-modes (car pair) (cdr pair))))
	      path-collector)
	(mapcar #'car path-collector)))))


(provide 'tangle-with-publish-dir)
