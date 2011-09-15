#!/usr/bin/env python

import itertools

## changes required to lilypond paper definitions
'''
--- /usr/share/lilypond/2.12.3/scm/paper.scm.orig	2011-04-21 06:28:10.000000000 -0500
+++ /usr/share/lilypond/2.12.3/scm/paper.scm	2011-03-25 17:07:50.000000000 -0500
@@ -211,6 +211,8 @@
     ("pa10" . (cons (* 26 mm) (* 35 mm)))
     ;; F4 used in southeast Asia and Australia
     ("f4" . (cons (* 210 mm) (* 330 mm)))
+    ;; Custom Sizes
+    ("letter-by-8" . (cons (* 4.25 in) (* 2.75 in)))
    ))
 
 ;; todo: take dimension arguments.
'''

rhythms = [
    ('A','Taka Taka Stop Stop', 'z16 z z z z8-. z-.', 7),
    ('B','Ice Cream Shh Cone','z8-. z-. r z-.', 4.5),
    ('C','Stop Pony Stop Pony','z8-. z16 z z8-. z16 z ', 7),
    ('D','Pineapple Pineapple','\\times 2/3 {z8 z z} \\times 2/3 {z8 z z}', 6.5),
    ('E','Peanut Butter Peanut Butter','z16 z z z z z z z', 8.5)]

lilypond_template = """
\\version "2.12.3"

\\include "english.ly"

#(set-global-staff-size 100)

\paper {
  tagline = ##f
  #(set-paper-size "letter" 'landscape)
  system-count = 1
  print-page-number = ##f
  line-width = %s \\in
  indent = #0
}

\\score {
  \\new Staff {
    \\clef treble
    <<    
    \\new Voice {
        \\hideNotes
        g''''8
    }
    \\new Voice {
        %s
    }
    >>
  }
  \\layout {
    ragged-right = ##t
    \\context {
      \\Staff
      \\remove "Time_signature_engraver"
      \\remove "Bar_engraver"
      \\remove "Staff_symbol_engraver"
      \\remove "Clef_engraver"
    }
  }
}
"""
       
if __name__ == "__main__":
    for v,n,r,w in rhythms:
        cmd = """lilypond -o"Twinkle %s %s" --pdf - << EOF\n%s\nEOF""" % (v, n,(lilypond_template % (w,r.replace('z','e\''))))
        print cmd
