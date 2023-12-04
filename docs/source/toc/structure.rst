Software structure
==================

As a GUI software, broh5 is designed based on the Model-View-Controller (MVC)
design pattern which is a widely used architectural paradigm in GUI development. It
separates an application into three interconnected components; improving modularity,
scalability, and maintainability. However, the traditional MVC terminology
may be non-intuitive for general users, Broh5 adapts these concepts with
more user-friendly naming:

-   **Rendering module**: This is only responsible for constructing and
    rendering GUI components.
-   **Utilities module**: Operating independently, this module provides utility
    methods for data handling, representation, and preparation.
-   **Interactions module**: This acts as a bridge, linking user interactions
    with GUI responses.

    .. image:: figs/fig_02.png
      :width: 100 %
      :align: center

To separate the rendering and interactions modules, Broh5 uses
`class inheritance <https://www.w3schools.com/python/python_inheritance.asp>`__,
which is a very powerful tool for developing complex applications.
