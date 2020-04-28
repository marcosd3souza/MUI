function obj = readtable(file, varargin)

  if nargin >= 1
      [~, n, e, ~] = fileparts(file);
      sep = ',';
      heads = 0;
  end

  if nargin >=2
    # check for delimiter
    DelimiterIndex = find( strcmp( varargin, 'delimiter' ) == 1);
    if isempty(DelimiterIndex)
      sep = ',';
    else
      sep = varargin{DelimiterIndex + 1};
    end

    # check for headers
    HeaderIndex = find( strcmp( varargin, 'HeaderLines' ) == 1);
    if isempty(HeaderIndex)
      heads = 0;
    else
      heads = varargin{HeaderIndex + 1};
    end

  end

  # open file
  if strcmp(e, '.xlsx')
    ret = xlsread(file);
  else
    ret = read_file(file, sep, heads);
  end

  if heads == 0
    try
      obj = table(ret(2:end,:), 'VariableNames', ret(1,:));
    catch
      obj = table(ret, 'VariableNames', {n});
    end
  else
      obj = table(ret, 'VariableNames', 'Var');
  end

end

function ret = read_file(file, sep, heads)
  # open file
  f = fopen(file);
  if f < 3
    error('Unable to open file')
    return
  end


  # skip headers
  if heads > 0
    for n = 1:heads
      fgetl(f);
    end
  end

  # count separators
  mark = ftell(f);
  tmp = fgetl(f);
  num_sep = numel(strfind(tmp,sep));
  fseek(f, mark, 'bof');

  # read values
  ret = fread (f, 'char=>char').';

  # check end of line
  if tmp(end)~=sep
    ret = regexprep (ret,'\n',[sep '\n']);
    num_sep = num_sep + 1;
  end
  # remove all newlines
  ret=regexprep (ret,'(\n)+','');

  # parsing values
  ret = regexp(ret,sep,'split');

  # format output
  # delete empty last field
  if mod(size(ret,2),num_sep)~=0
    # yes, because we split after each separator
    if numel(ret{1,end}) == 0
      ret = ret(1,1:end-1);
    end

    if mod(size(ret,2),num_sep)==0
      ret = reshape (ret,num_sep,[])';
    end
  else
    ret = reshape (ret,num_sep,[])';
  end


end
