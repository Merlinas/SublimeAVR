# AVR Sublime Text 2/3 plug-in

## Installation

**Prerequisites**

- Make sure that you have installed [Atmel AVR Toolchain](http://www.atmel.com/tools/atmelavrtoolchainforwindows.aspx) and set it in PATH (or use the plug-in settings to prepend the PATH).
- In Windows you probably have to install Make as well. [Make for Windows](http://gnuwin32.sourceforge.net/packages/make.htm) is probably the best option.

**Manual installation**

- Download and unzip, or git clone, the plug-in into `Packages/SublimeAVR` folder. To access the folder called `Packages`, open Sublime Text and select *Preferences*, *Browse packages...*
- Note that the plug-in can't be installed *in the Sublime Text 3 way* in to the `Installed Packages` folder.

## Usage

Press `CTRL+SHIFT+P` to bring the command palette into view. Next type
*AVR* and select a command which to run:

- __Create New Project__: Prompts the MCU type and directory where to create a new project.
  When done you can open the project file located under the directory where ever you created the project.
  To do that select *Project*, *Open projects...*, browse to the project folder and double click
  `SublimeAVR.sublime-project` file.

### Shortcut keys

- `CTRL+B` builds the project
- `ALT+D ALT+D` goes to the definition of whatever is under the current cursor position
- `ALT+D ALT+I` goes to the implementation of whatever is under the current cursor position
- `ALT+D ALT+B` come back to where ever you were before hitting goto the definition or implementation


### Settings

To edit plug-in settings select *Preferences*, *Package Settings*, *AVR*. If you don't want to alter the default settings, copy and paste those into the user side for editing.

- __c_std__ and __cpp_std__: C and C++ standard used when creating the project. These settings have affect to preprocessor define macros saved into `SublimeAVR.sublime-project` file.
- __optimize__: Compiler optimization level. Has also affect to preprosessor define macros.
- __path__: The project PATH environment variable will be prepended with this.


## Plug-in Dependencies

SublimeAVR plug-in is dependent of [SublimeClang](https://github.com/quarnster/SublimeClang)
plug-in. This dependent plug-in will be installed automatically by the SublimeAVR plug-in if
needed. If you decided to pre-install SublimeClang, SublimeAVR will notice this and will
not overwrite or modify your installation.

## License

This SublimeAVR Sublime Text plug-in is licensed under the MIT license:

> Copyright (c) 2014 Kim Blomqvist, kblomqvist.github.io
> 
> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the Software is
> furnished to do so, subject to the following conditions:
> 
> The above copyright notice and this permission notice shall be included in
> all copies or substantial portions of the Software.
> 
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
> THE SOFTWARE.

The plug-in is derived from Aery32 Sublime Text plug-in, which is licensed under
the new BSD license:

> Copyright (c) 2012-2013, Muiku Oy
> All rights reserved.
> 
> Redistribution and use in source and binary forms, with or without modification,
> are permitted provided that the following conditions are met:
> 
>    * Redistributions of source code must retain the above copyright notice,
> 	 this list of conditions and the following disclaimer.
> 
>    * Redistributions in binary form must reproduce the above copyright notice,
> 	 this list of conditions and the following disclaimer in the documentation
> 	 and/or other materials provided with the distribution.
> 
>    * Neither the name of Muiku Oy nor the names of its contributors may be
> 	 used to endorse or promote products derived from this software without
> 	 specific prior written permission.
> 
> THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
> ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
> WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
> DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
> ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
> (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
> LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
> ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
> (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
> SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

SublimeClang is licensed under the zlib:

> Copyright (c) 2011-2012 Fredrik Ehnbom
>
> This software is provided 'as-is', without any express or implied
> warranty. In no event will the authors be held liable for any damages
> arising from the use of this software.
>
> Permission is granted to anyone to use this software for any purpose,
> including commercial applications, and to alter it and redistribute it
> freely, subject to the following restrictions:
>
>   1. The origin of this software must not be misrepresented; you must not
>   claim that you wrote the original software. If you use this software
>   in a product, an acknowledgment in the product documentation would be
>   appreciated but is not required.
>
>   2. Altered source versions must be plainly marked as such, and must not be
>   misrepresented as being the original software.
>
>   3. This notice may not be removed or altered from any source
>   distribution.
