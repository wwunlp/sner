Working with ATF
================

This is intended to be reference for those working with ``sner`` and ``.atf``,
based on material from the
`cdli <http://cdli.ucla.edu/?q=support-cdli>`_ and
`oracc <http://oracc.museum.upenn.edu/doc/help/editinginatf>`_.
Sections are organized by first character in line.

``&``
-----

``&P329447 = CUSAS 03, 0001``: Beginning of a text with CDLI ID and name.

``#``
-----

- ``#project: cams``: Project of text. Unique to Oracc.
- ``atf: lang akk`` or ``#atf: lang akk-x-stdbab``: Language of text.
  CDLI and Oracc, yet Oracc uses ``sux`` for Sumerian like the CDLI.
- ``atf: use unicode``: Unique to Oracc. CDLI uses ASCII.
- ``tr.en:``: Transliteration of text.
- Other ``#`` lines are comment lines.

``@``
-----

Object type

- ``@tablet``
- ``@envelope``
- ``@prism``
- ``@bulla``
- ``@fragment``
- ``@object`` - generic tag, i.e. ``@object cone`` or ``@object seal``

Surfaces & locations

- ``@observe``
- ``@reverse``
- ``@left``, ``@right``, ``@top``, ``@bottom``
- ``@face``
- ``@surface`` - generic tag, i.e. ``@surface side a``
- ``@edge``
- ``@seal``
- ``@column``

Discourse

- ``@catchline``
- ``@colophon``
- ``@date``
- ``@signatures``, ``@signature``
- ``@summary``
- ``@witnesses``

``$``
-----

- Breakage
- Blank lines
- Qualification
- Number
- Scope
- State
- Ruling
- Image location

Text
----

``1. 3(disz) gurusz szitim``: Number, period, space, then line.
Line continuation is space, then line.

``>>``
------

``>>Q001075 001``: Reference to Oracc
`Q-catalogue <http://oracc.museum.upenn.edu/qcat>`_
ID and line number.
