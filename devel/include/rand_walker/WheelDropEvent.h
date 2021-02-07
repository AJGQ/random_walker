// Generated by gencpp from file rand_walker/WheelDropEvent.msg
// DO NOT EDIT!


#ifndef RAND_WALKER_MESSAGE_WHEELDROPEVENT_H
#define RAND_WALKER_MESSAGE_WHEELDROPEVENT_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace rand_walker
{
template <class ContainerAllocator>
struct WheelDropEvent_
{
  typedef WheelDropEvent_<ContainerAllocator> Type;

  WheelDropEvent_()
    : wheel(0)
    , state(0)  {
    }
  WheelDropEvent_(const ContainerAllocator& _alloc)
    : wheel(0)
    , state(0)  {
  (void)_alloc;
    }



   typedef uint8_t _wheel_type;
  _wheel_type wheel;

   typedef uint8_t _state_type;
  _state_type state;



// reducing the odds to have name collisions with Windows.h 
#if defined(_WIN32) && defined(LEFT)
  #undef LEFT
#endif
#if defined(_WIN32) && defined(RIGHT)
  #undef RIGHT
#endif
#if defined(_WIN32) && defined(RAISED)
  #undef RAISED
#endif
#if defined(_WIN32) && defined(DROPPED)
  #undef DROPPED
#endif

  enum {
    LEFT = 0u,
    RIGHT = 1u,
    RAISED = 0u,
    DROPPED = 1u,
  };


  typedef boost::shared_ptr< ::rand_walker::WheelDropEvent_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::rand_walker::WheelDropEvent_<ContainerAllocator> const> ConstPtr;

}; // struct WheelDropEvent_

typedef ::rand_walker::WheelDropEvent_<std::allocator<void> > WheelDropEvent;

typedef boost::shared_ptr< ::rand_walker::WheelDropEvent > WheelDropEventPtr;
typedef boost::shared_ptr< ::rand_walker::WheelDropEvent const> WheelDropEventConstPtr;

// constants requiring out of line definition

   

   

   

   



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::rand_walker::WheelDropEvent_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::rand_walker::WheelDropEvent_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::rand_walker::WheelDropEvent_<ContainerAllocator1> & lhs, const ::rand_walker::WheelDropEvent_<ContainerAllocator2> & rhs)
{
  return lhs.wheel == rhs.wheel &&
    lhs.state == rhs.state;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::rand_walker::WheelDropEvent_<ContainerAllocator1> & lhs, const ::rand_walker::WheelDropEvent_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace rand_walker

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsFixedSize< ::rand_walker::WheelDropEvent_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::rand_walker::WheelDropEvent_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::rand_walker::WheelDropEvent_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::rand_walker::WheelDropEvent_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::rand_walker::WheelDropEvent_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::rand_walker::WheelDropEvent_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::rand_walker::WheelDropEvent_<ContainerAllocator> >
{
  static const char* value()
  {
    return "e102837d89384d67669a0df86b63f33b";
  }

  static const char* value(const ::rand_walker::WheelDropEvent_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xe102837d89384d67ULL;
  static const uint64_t static_value2 = 0x669a0df86b63f33bULL;
};

template<class ContainerAllocator>
struct DataType< ::rand_walker::WheelDropEvent_<ContainerAllocator> >
{
  static const char* value()
  {
    return "rand_walker/WheelDropEvent";
  }

  static const char* value(const ::rand_walker::WheelDropEvent_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::rand_walker::WheelDropEvent_<ContainerAllocator> >
{
  static const char* value()
  {
    return "# wheel\n"
"uint8 LEFT  = 0\n"
"uint8 RIGHT = 1\n"
"\n"
"# state\n"
"uint8 RAISED  = 0\n"
"uint8 DROPPED = 1\n"
"\n"
"uint8 wheel\n"
"uint8 state\n"
;
  }

  static const char* value(const ::rand_walker::WheelDropEvent_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::rand_walker::WheelDropEvent_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.wheel);
      stream.next(m.state);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct WheelDropEvent_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::rand_walker::WheelDropEvent_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::rand_walker::WheelDropEvent_<ContainerAllocator>& v)
  {
    s << indent << "wheel: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.wheel);
    s << indent << "state: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.state);
  }
};

} // namespace message_operations
} // namespace ros

#endif // RAND_WALKER_MESSAGE_WHEELDROPEVENT_H
