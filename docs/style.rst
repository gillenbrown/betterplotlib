.. _api_ref:

.. currentmodule:: betterplotlib

.. _tools_api:

Styles
==================================

Betterplotlib has multiple style options that make plots look better in 
general. `default_style()` is the best choice for everyday usage. 
`presentation_style()` makes font larger for easily readable presentations.
`white_style()` also makes the text larger, but also makes lines white, so they
are visible against a dark background in a presentation.

The following table shows which parameters are set in which style.

Font Options
---------------

+--------------------+------------+---------------+-------+
| Parameter          | Default    | Presentation  | White |
+====================+============+===============+=======+ 
| `font.family`      | sans-serif                         |
+--------------------+------------+---------------+-------+
| `font.sans-serif`  | Helvetica Neue                     |
+--------------------+------------+---------------+-------+
| `font.weight`      | bold                               |
+--------------------+------------+---------------+-------+
| `axes.labelweight` | bold                               |
+--------------------+------------+---------------+-------+
| `axes.titleweight` | bold                               |
+--------------------+------------+---------------+-------+
| `axes.titlesize`   | 16         | 20                    |
+--------------------+------------+---------------+-------+
| `font.size`        | 14         | 18                    |
+--------------------+            |                       +
| `axes.labelsize`   |            |                       |
+--------------------+------------+---------------+-------+
| `xtick.labelsize`  | 12         | 16                    |
+--------------------+            |                       +
| `ytick.labelsize`  |            |                       |
+--------------------+------------+---------------+-------+
| `legend.fontsize`  | 13         | 17                    |
+--------------------+------------+---------------+-------+
| `text.color`       | bpl.almost_black           | white |
+--------------------+------------+---------------+-------+

Colors
------

+--------------------+------------+---------------+-----------------------------------------+
| Parameter          | Default    | Presentation  | White                                   |
+====================+============+===============+=========================================+ 
| `patch.edgecolor`  | bpl.almost_black           | white                                   |
+--------------------+                            |                                         +
| `axes.edgecolor`   |                            |                                         |
+--------------------+                            |                                         +
| `axes.labelcolor`  |                            |                                         |
+--------------------+                            |                                         +
| `xtick.color`      |                            |                                         |
+--------------------+                            |                                         +
| `xtick.color`      |                            |                                         |
+--------------------+                            |                                         +
| `grid.color`       |                            |                                         |
+--------------------+------------+---------------+-----------------------------------------+
| color cycle        | Modified Tableau 10        | white, yellow, then Modified Tableau 10 |
+--------------------+------------+---------------+-----------------------------------------+
| `image.cmap`       | Viridis                                                              |
+--------------------+------------+---------------+-----------------------------------------+

Other
-----

These other parameters are constant for all styles.

+----------------------------+---------+
| Parameter                  | Value   |
+============================+=========+ 
| `legend.scatterpoints`     | 1       |
+----------------------------+---------+
| `savefig.format`           | pdf     |
+----------------------------+---------+
| `axes.formatter.useoffset` | False   |
+----------------------------+---------+
| `figure.figsize`           | [10, 7] |
+----------------------------+---------+

API
---

The following show the ways to set each style. 

.. autofunction:: default_style

.. autofunction:: presentation_style

.. autofunction:: white_style