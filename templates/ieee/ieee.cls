% ModuTex v1.0 - IEEE Template Class
% Simplified IEEE class file for demonstration
% In production, use the official IEEE template from IEEE Xplore

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{ieee}[2024/01/01 IEEE Template for ModuTex]

% Load base class
\LoadClass[10pt,conference]{article}

% Required packages
\RequirePackage{times}
\RequirePackage{graphicx}
\RequirePackage{amsmath}
\RequirePackage{amssymb}
\RequirePackage{cite}

% Page layout
\setlength{\textheight}{8.875in}
\setlength{\textwidth}{6.875in}
\setlength{\columnsep}{0.3125in}
\setlength{\topmargin}{0in}
\setlength{\headheight}{0in}
\setlength{\headsep}{0in}
\setlength{\parindent}{1pc}

% Two column mode
\twocolumn
\sloppy

% IEEE style modifications
\def\@maketitle{%
  \newpage
  \null
  \vskip 2em%
  \begin{center}%
  \let \footnote \thanks
    {\LARGE \@title \par}%
    \vskip 1.5em%
    {\large
      \lineskip .5em%
      \begin{tabular}[t]{c}%
        \@author
      \end{tabular}\par}%
    \vskip 1em%
    {\large \@date}%
  \end{center}%
  \par
  \vskip 1.5em}

% Section formatting
\renewcommand\section{\@startsection{section}{1}{\z@}%
                     {-3.5ex \@plus -1ex \@minus -.2ex}%
                     {2.3ex \@plus.2ex}%
                     {\normalfont\large\bfseries}}

\endinput 