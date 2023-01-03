\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{myclass}

% Article One column
\LoadClass[]{article}
\RequirePackage[a4paper, total={6in, 9in}]{geometry}

% Article Two column
%\LoadClass[twocolumn]{article}
%\RequirePackage[a4paper, total={7in, 9in}]{geometry}

\setlength{\columnseprule}{0pt}
\setlength{\columnsep}{1.5cm}

% Custom symbols
\newcommand{\e}{\mathrm{e}}
\newcommand{\im}{\mathrm{i}}
\newcommand{\arcangle}{\mathord{<\mspace{-9mu}\mathrel{)}\mspace{2mu}}}
\renewcommand{\thefootnote}{\fnsymbol{footnote}}

% Colouring
\RequirePackage[]{hyperref}
\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    filecolor=blue,      
    urlcolor=blue,
    }

% Packages
\usepackage{amssymb}
\usepackage{amsmath, amsfonts, enumerate, graphicx, hyperref, 
            mathrsfs, physics, wasysym, xcolor}

% Additional packages and commands depending on project:
\usepackage{lipsum, subcaption, caption, listings, color}

\definecolor{mygreen}{rgb}{0,0.6,0}
\definecolor{mygray}{rgb}{0.5,0.5,0.5}
\definecolor{mymauve}{rgb}{0.58,0,0.82}

\lstset{ %
  backgroundcolor=\color{white},   % choose the background color
  basicstyle=\footnotesize\ttfamily,        % size of fonts used for the code
  breaklines=true,                 % automatic line breaking only at whitespace
  captionpos=b,                    % sets the caption-position to bottom
  commentstyle=\color{mygreen},    % comment style
  escapeinside={\%*}{*)},          % if you want to add LaTeX within your code
  keywordstyle=\color{blue},       % keyword style
  stringstyle=\color{mymauve},     % string literal style
}
