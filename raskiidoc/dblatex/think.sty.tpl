%%
%% This style is derived from the docbook one.
%%
\NeedsTeXFormat{LaTeX2e}
\ProvidesPackage{asciidoc-dblatex}[2012/10/24 AsciiDoc DocBook Style]

% this will set letterpaper, because docbook.sty honors page layout
% made by geometry package
\usepackage[letterpaper,total={21cm,29.7cm}, top=1in, left=0.75in, right=0.75in, bottom=0.75in]{geometry}

%% Just use the original package and pass the options.
\RequirePackageWithOptions{docbook}

\newlength\mylength
\def\blueribbon{
   \setlength\mylength{0.3\paperheight}
  \AddToShipoutPicture*{
     \put(0,\LenToUnit{\mylength}){%
       {\color{blue}\rule{\paperwidth}{1cm}}}
   }
}

\chead[]{}
\lhead[]{}
\rhead[]{\@ifundefined{chaptername}{test chapter name}{\chaptername}}
\lfoot[]{\@ifundefined{DBKpublisher}{<%= $conf["vars::Pages::FooterLeft"] %>}{\DBKpublisher}}
\rfoot[]{\@ifundefined{DBKpublisher}{<%= $conf["vars::Pages::FooterRight"] %>}{\DBKpublisher}}
\cfoot[]{\textsf{<%= $conf["vars::Pages::FooterCenter"] %>}}

% custom cover page
\def\DBKcover{
  \ifthenelse{\equal{\DBKedition}{}}{\def\edhead{}}{\def\edhead{Ed. \DBKedition}}
  \thispagestyle{empty}
  \begin{flushright}
  <% if not $conf["vars::CoverPage::Logo1Filename"].nil? %>
  \includegraphics[width=<%= $conf["vars::CoverPage::Logo1Size"] %>\textwidth]{<%= $conf["vars::CoverPage::Logo1Filename"] %>}
  <% end %>
  \vspace*{1in}
  \bfseries
  \sffamily
  {\Huge \DBKtitle \\[1ex]\large ~~~ \\}
  \vspace*{2.1in}
  {\color{blue} \Huge ~~~ \\ \huge ~~~ \\}
  \vspace*{2.1in}
  {\Large\DBKdate \\}
  \end{flushright}
  \vfill
  \begin{center}{\Large \bfseries \sffamily Th!nk}\end{center}
  \blueribbon
}

% use different charter and inconsolata roman and typewriter fonts
\usepackage{charter}
\usepackage{inconsolata}

% re-set the listing environment, because we changed tt font and we
% don't want colored background
% \lstset{%
%     basicstyle=\ttfamily\small, %
%     backgroundcolor={}%
% }
