#!/usr/bin/env ruby

@values = Array.new

STDIN.read.split("\n").each do |a|
   if a =~ /(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+([\w+.$]+)/
					 id = $1
					 tstart = $2
					 tend  = $3
					 gstart = $4
					 gend = $5
					 excl = $6
					 incl = $7
					 meth = $8
					 #if stt =~ /[^\w]+([\w\d_.]+)$/
					 #				 function = $1
					 #end
					 #if time =~ /(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?(?:(\d+)ms)/
					#				 h  = $1 != nil ? $1 : "0"
					#				 m  = $2 != nil ? $2 : "0"
					#				 s  = $3 != nil ? $3 : "0"
					#				 ms = $4 != nil ? $4 : "0"
					#				 time = "#{h}:#{m}:#{s}.#{ms}"
					 #end
					 @values << "#{id},#{tstart},#{tend},#{gstart},#{gend},#{excl},#{incl},#{meth}"
	 end
end

# puts "pid,tstart,tend,gstart,gend,excl,incl,meth"
puts "#{@values.join("\n")};"
