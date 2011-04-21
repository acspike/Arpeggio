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

lilypond_template = """
\\version "2.12.3"

\\include "english.ly"

#(set-global-staff-size 30)

\paper {
  tagline = ##f
  #(set-paper-size "letter-by-8")
  system-count = 1
  print-page-number = ##f
  line-width = 1 \\in
  indent = #0
}

\\score {
  \\new Staff {
    \\clef %s
    <<
    \\new Voice {
        \\hideNotes
        %s8
        %s8
    }
    \\new Voice {
        %s4
    }
    >>
  }
  \\layout {
    ragged-right = ##t
    \\context {
      \\Staff
      \\remove "Time_signature_engraver"
      \\remove "Bar_engraver"
    }
  }
}
"""
clefs = {
'treble' :(lambda note: lilypond_template % ('treble',"e''''","e''''", note)),
'bass' :(lambda note: lilypond_template % ('bass',"g''","g''", note))
}

octaves = [",,,",",,",",","","'","''","'''","''''"]
notes = [n+a for n in 'cdefgab' for a in ['flat','','sharp']]
notes = 'cdefgab'
def note_range(start_note, start_octave, end_note, end_octave):
    end = (end_note,end_octave)
    start_index = notes.index(start_note)
    note_octave_iter = ((n,o) for o in xrange(start_octave,end_octave+1) for n in notes)
    note_iter = (n for n in itertools.dropwhile(lambda x: x[0]!=start_note, note_octave_iter))
    
    result = ()
    while result != end:
        result = note_iter.next()
        yield result

       
def make_pdfscript(clef, start_note, start_octave, end_note, end_octave):
    for note, octave_number in note_range(start_note, start_octave, end_note, end_octave):
        cmd = "lilypond -o%s%s%s --pdf - << EOF\n%s\nEOF" % (clef,note,octave_number,clefs[clef](note+octaves[octave_number]))
        print cmd
        
        
        
if __name__ == "__main__":
    make_pdfscript('treble', "e",2,"e",7)
    make_pdfscript('bass', "b",0,"g",5)
        
