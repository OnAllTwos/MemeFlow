# MemeFlow
A FlowLauncher plugin for generating memes

Uses [MemePy](https://github.com/julianbrandt/MemePy)

## Syntax
First, use the activation keyword `mf` followed by the name of a template, then a list of arguments delimited by `|`.

```
mf TEMPLATE_NAME argument1|argument2|...
```

Default available templates can be found [here](https://github.com/julianbrandt/MemePy#built-in-template-docs)

Arguments may be either text or images. For images, provide the link to the image within angle brackets.

```
mf TEMPLATE_NAME <http://path.to/my_image.jpg>|some text
```
