% ModuTex v1.0 - Elsevier Template Class  
% Simplified Elsevier class file for demonstration
% In production, use the official elsarticle.cls from Elsevier

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{elsarticle}[2024/01/01 Elsevier Template for ModuTex]

% Load base class
\LoadClass[12pt]{article}

% Required packages
\RequirePackage{graphicx}
\RequirePackage{amsmath}
\RequirePackage{amssymb}
\RequirePackage{natbib}
\RequirePackage{geometry}

% Page geometry
\geometry{
    a4paper,
    left=2.5cm,
    right=2.5cm,
    top=2.5cm,
    bottom=2.5cm
}

% Title formatting
\def\@maketitle{%
  \newpage
  \null
  \vskip 2em%
  \begin{center}%
  \let \footnote \thanks
    {\LARGE \bfseries \@title \par}%
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

% Abstract environment
\renewenvironment{abstract}{%
    \small
    \begin{center}%
    {\bfseries Abstract\vspace{-.5em}\vspace{\z@}}%
    \end{center}%
    \quotation
}{%
    \endquotation
}

% Keywords environment
\newenvironment{keywords}{%
    \small
    \textbf{Keywords:} 
}{%
    \par
}

% Section formatting
\renewcommand\section{\@startsection{section}{1}{\z@}%
                     {-3.5ex \@plus -1ex \@minus -.2ex}%
                     {2.3ex \@plus.2ex}%
                     {\normalfont\Large\bfseries}}

\endinput 