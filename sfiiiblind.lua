--memory locations based on the following community leaders:
-- sf3lp's training mode
-- c_cube's hitbox viewer

local SCREEN_WIDTH          = 384
local SCREEN_HEIGHT         = 224
local GAME_PHASE_PLAYING    = 2

local address = {
	player1         = 0x02068C6C,
	player2         = 0x02069104,
	screen_center_x = 0x02026CB0,
	game_phase      = 0x020154A6
}
local globals = {
	game_phase      = 0,
	screen_center_x = 0,
	num_misc_objs   = 0
}
local player1 = {}
local player2 = {}
local misc_objs = {}


function update_globals()
	globals.screen_center_x = memory.readword(address.screen_center_x)
	globals.game_phase      = memory.readword(address.game_phase)
end

function pos_players()
	--expected line format: "p1xpos p1ypos p2xpos p2ypos p1hp p2hp time"
	file = io.open("buffer.txt", "a")
	file:write(player1.pos_x, " ", player1.pos_y, " ", player2.pos_x, " ")
	file:write(player2.pos_y, " ", player1.health, " ", player2.health, " ", memory.readbyte(0x02011377), "\n")
	io.close(file)
end

function update_players(obj, base)
	obj.facing_dir   = memory.readbyte(base + 0xA)
	obj.opponent_dir = memory.readbyte(base + 0xB)
	obj.pos_x        = memory.readword(base + 0x64)
	obj.pos_y        = memory.readword(base + 0x68)
	obj.anim_frame   = memory.readword(base + 0x21A)
	obj.health       = memory.readbyte(base + 0x9F)
end


function send_info()
	update_globals()
	if globals.game_phase ~= GAME_PHASE_PLAYING then
		gui.clearuncommitted()
		return
	end

	update_players(player1, address.player1)
	update_players(player2, address.player2)
	pos_players()

end

file = io.open("buffer.txt","w")
file:write("")
file:close()
gui.register( function()
	send_info()
end)