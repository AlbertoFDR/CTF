## ProjectSekai - Scanner Service (100p)
### Solved by [Maiky](https://github.com/maikypedia).

In this CTF challenge, the web platform allow us to scan an IP:PORT pair using the nmap tool. The goal of this kind of challenge is used to achieve RCE.

File `src/app/controllers/scanner.rb`:

``` ruby
  post '/' do
    input_service = escape_shell_input(params[:service])
    hostname, port = input_service.split ':', 2
    begin
      if valid_ip? hostname and valid_port? port
        # Service up?
        s = TCPSocket.new(hostname, port.to_i)
        s.close
        # Assuming valid ip and port, this should be fine
        @scan_result = IO.popen("nmap -p #{port} #{hostname}").read
      else
        @scan_result = "Invalid input detected, aborting scan!"
      end
    rescue Errno::ECONNREFUSED
      @scan_result = "Connection refused on #{hostname}:#{port}"
    rescue => e
      @scan_result = e.message
    end
```

File: `src/app/helper/scanner_helper.rb`

``` ruby
    def valid_port?(input)
      # ----------------------------------------
      # HERE IS THE VULNERABILITY 
      # If the port start with integer it works
      # ----------------------------------------
      !input.nil? and (1..65535).cover?(input.to_i)
    end

    # def valid_ip?(input) 
    # ...
    
    # def escape_shell_input(input_string)
    # ...

```

In this case, the other vulnerable function is `escape_shell_input` which escapes a lot of the possible Command Injection techniques. It escapes the following ones: ' ' '$' '\`' '"' '\\' '|' '&' ';' '<' '>' '(' ')' "'" "\n" "*". The problem is that it doesn't escape the tab char that allow us to use it as an space. So, in this case we can add arguments in the exec. For the final solution, we need to use the scripts feature of Nmap. In other words, we need to upload a Lua script using `http-fetch` ([link](https://gtfobins.github.io/gtfobins/nmap/)) and then execute it. The final exploit is `solve.py` that uploads the `flag.nse` scripts and executes it.
