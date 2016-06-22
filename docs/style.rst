.. _api_ref:

.. currentmodule:: betterplotlib.tools

.. _tools_api:

Styles
==================================

Betterplotlib has multiple style options that make plots look better in 
general. `default_style()` is the best choice for everyday usage. 
`presentation_style()` makes font larger for easily readable presentations.
`white_style()` also makes the text larger, but also makes lines white, so they
are visible against a dark background in a presentation.

The following table shows which parameters are set in which style.

+--------------------+------------+---------------+-------+
|  Font Options                                           |
+====================+============+===============+=======+ 
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
+--------------------+------------+---------------+-------+
| `axes.labelsize`   | 14         | 18                    |
+--------------------+------------+---------------+-------+
| `xtick.labelsize`  | 12         | 16                    |
+--------------------+------------+---------------+-------+
| `ytick.labelsize`  | 12         | 16                    |
+--------------------+------------+---------------+-------+
| `legend.fontsize`  | 13         | 17                    |
+--------------------+------------+---------------+-------+
| `text.color`       | bpl.almost_black           | white |
+--------------------+                            |       |
| `patch.edgecolor`  |                            |       |
+--------------------+------------+---------------+-------+



.. autofunction:: default_style

.. autofunction:: presentation_style

.. autofunction:: white_style